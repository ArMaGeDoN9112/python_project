var socker;
var file;
var fileSpan = document.getElementById("file-span");

function start() {
    console.log(file);
    if (file == undefined) {
        file = document.getElementById("file").files[0];
    }

    if (file == undefined) {
        alert("Please, put file!")
        return;
    }

    setCanUpload(false);

    let formData = new FormData();

    formData.append("file", file);

    var div = document.getElementById("text");
    while(div.firstChild) {
        div.removeChild(div.firstChild);
    }

    fetch("/api/upload-file", {method: "POST", "body": formData})
        .then((response) => response.json())
        .then((json) => runListener(json.key))
}

function setCanUpload(can) {
    canUpload = can;

    if (!can) {
        document.getElementById('send-file').style.color = "grey";
    }
    else {
        document.getElementById('send-file').style.color = null;
    }
}

var use_colors = false;
document.getElementById("emotion_toggle").onclick = () => {
    use_colors = !use_colors;
}


function colorFromNum(num) {
    switch (num) {
        case "0":
            return "#AB2524";
        case "1":
            return "#6F4F28";
        case "2":
            return "#FFA421";
        case "3":
            return "#48A43F";
        case "4":
            return "#9DA3A6";
        case "5":
            return "#3481B8";

        default:
            return "#ffffff";
    }
}

function runListener(key) {
    socket = new WebSocket('/api/analyze');
    // document.getElementById("phint-text").style.visibility = "hidden";

    console.log(use_colors);

    use_statistic = document.getElementById("statistic_enabler").checked;
    download_file = document.getElementById("download_file_enabler").checked;
    
    socket.onmessage = (ev) => {

        console.log('<<< ' + ev.data, 'blue');

        data = JSON.parse(ev.data)

        if (data.string != undefined) {
            var span = document.createElement("span");
            
            var str = data.string.split("@")[0]
            var color = colorFromNum(data.string.split("@")[1].trim())
            
            span.style = "background-color: " + color + ";" + "\nopacity: 0.7";
            span.className = "_text"
            span.textContent = str + " ";

            document.getElementById("text").appendChild(span);
        }

        console.log(JSON.parse(ev.data))
    };

    socket.onclose = () => {
        console.log("CLOSE!");
        file = undefined;
        document.getElementById('send-file').disabled = false;
        setCanUpload(true);

        if (use_statistic) {
            fetch("/api/get-statistic/"+key, {
          method: "GET"
        })
          .then((response) => response.blob())
          .then((blob) => {
            const imageUrl = URL.createObjectURL(blob);
            const imageElement = document.createElement("img");
            imageElement.src = imageUrl;
            imageElement.style = "width: 620px";
            const container = document.getElementById("text");
            container.appendChild(imageElement);
          })
        }

        if (download_file) {
            fetch("/api/download-file/"+key, {
                method: "GET"
              })
                .then((response) => response.blob())
                .then((blob) => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = key;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                })
        }
    }

    socket.onopen = () => {
        socket.send(key);
        socket.send(use_colors);
        socket.send(use_statistic);
    };
}

document.getElementById('send-file').onclick = ev => {
    if (!canUpload) {
            alert("You can't use it right now!")
            return;
    }
    ev.preventDefault();
    start();
};

document.getElementById("file").addEventListener("change", () => {
    fileSpan.textContent = document.getElementById("file").files[0].name;
})

var canUpload = true;
document.getElementById('upload_file').onclick = ev => {
    document.getElementById("file").click()
};

const dropZone = document.body;
if (dropZone) {
    let hoverClassName = 'hover';
  
    dropZone.addEventListener("dragenter", function(e) {
        e.preventDefault();
        dropZone.classList.add(hoverClassName);
    });
  
    dropZone.addEventListener("dragover", function(e) {
        e.preventDefault();
        dropZone.classList.add(hoverClassName);
    });
  
    dropZone.addEventListener("dragleave", function(e) {
        e.preventDefault();
        dropZone.classList.remove(hoverClassName);
    });
  
    // Это самое важное событие, событие, которое дает доступ к файлам
    dropZone.addEventListener("drop", function(e) {
        e.preventDefault();
        dropZone.classList.remove(hoverClassName);

        const files = Array.from(e.dataTransfer.files);
        console.log(files);
        file = files[0];
        // TODO что-то делает с файлами...
    });
}