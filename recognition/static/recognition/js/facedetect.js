// In this case, We set width 320, and the height will be computed based on the input stream.
let width = 320;
let height = 240;
let imageAr=height/width

// whether streaming video from the camera.
let streaming = false;
let cascadeloded=false;

var video = document.querySelector("#videoElement");
let stream = null;
let vc = null;

videoJq=$("#videoElement")
canvasJq=$("#canvasOutput")

let src = null
let dst = null
let gray = null
let faces = null
let classifier = null

const FPS = 10;
let faceDetected=false;

function showCanvas(state){
  if(state){
    videoJq.addClass('hidden')
    canvasJq.removeClass('hidden')
  }
  else{
    canvasJq.addClass('hidden')
    videoJq.removeClass('hidden')
  }
}

let parentAr=canvasJq.parent().height()/canvasJq.parent().width();
  if(parentAr>imageAr){
     canvasJq.css('width', String(canvasJq.parent().width())+"px");
     canvasJq.css('height', String(canvasJq.parent().width()*imageAr)+"px");
  }
  else{
    canvasJq.css('height', String(canvasJq.parent().height())+"px");
    canvasJq.css('width', String(canvasJq.parent().height()/imageAr)+"px");
  }

$(window).resize(function(){
  let parentAr=canvasJq.parent().height()/canvasJq.parent().width();
  if(parentAr>imageAr){
     canvasJq.css('width', String(canvasJq.parent().width())+"px");
     canvasJq.css('height', String(canvasJq.parent().width()*imageAr)+"px");
  }
  else{
    canvasJq.css('height', String(canvasJq.parent().height())+"px");
    canvasJq.css('width', String(canvasJq.parent().height()/imageAr)+"px");
  }
});

function startCamera() {
  if (streaming) return;
  stopCamera()
  showCanvas(true);
  navigator.mediaDevices.getUserMedia({video: true, audio: false})
    .then(function(s) {
    stream = s;
    video.srcObject = s;
    video.play();
  })
    .catch(function(err) {
    console.log("An error occured! " + err);
  });

  video.addEventListener("canplay", function(ev){
    if (!streaming) {
      height = video.videoHeight / (video.videoWidth/width);
      video.setAttribute("width", width);
      video.setAttribute("height", height);
      streaming = true;
      vc = new cv.VideoCapture(video);
    }
    startVideoProcessing();
  }, false);
}


function detectFace(){
  vc.read(src);
  //src.copyTo(dst);
  cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY, 0);
  // detect faces.
  classifier.detectMultiScale(gray, faces, 2, 5, 0);
  // draw faces.
  let area=0;
  var rect=null;
  for (let i = 0; i < faces.size(); ++i) {
    let face = faces.get(i);
    if(area<face.width*face.height){
      rect=face;
      area=face.width*face.height;
    }
    else{
      continue
    }
  }
  if (area>0){
    let point1 = new cv.Point(rect.x, rect.y);
    let point2 = new cv.Point(rect.x + rect.width, rect.y + rect.height);
    cv.rectangle(src, point1, point2, [255, 0, 0, 255]);
    faceDetected=true;
  }
  else{
    faceDetected=false;
  }
}


function startVideoProcessing() {
  if (!streaming) { console.warn("Please startup your webcam"); return; }
  src = new cv.Mat(video.height, video.width, cv.CV_8UC4);
  gray = new cv.Mat();
  faces = new cv.RectVector();
  classifier = new cv.CascadeClassifier();
  // load pre-trained classifiers
  let utils = new Utils('errorMessage');
  let faceCascadeFile = 'haarcascade_frontalface_default.xml';
  if(classifier.load(faceCascadeFile))
  {
    requestAnimationFrame(processVideo);
  }else{
    console.log("cascade not loaded");
    utils.createFileFromUrl(faceCascadeFile, classifierUrl, () => {
        console.log('cascade ready to load.');
        classifier.load(faceCascadeFile);
        requestAnimationFrame(processVideo);
    });
  }
}




function processVideo() {
  let begin = Date.now();
  detectFace()
  cv.imshow("canvasOutput", src);
  let delay = 1000/FPS - (Date.now() - begin);
  setTimeout(processVideo, delay);
  //requestAnimationFrame(processVideo);
}



function stopCamera() {
  video.pause();
  showCanvas(false);
  video.srcObject=null;
  if(stream){
    stream.getVideoTracks()[0].stop();
  }
  streaming = false;
}


function opencvIsReady() {
  startCamera();
}