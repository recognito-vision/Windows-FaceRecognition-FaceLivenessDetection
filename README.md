<a href="https://recognito.vision" style="display: flex; align-items: center;">
    <img src="https://github.com/recognito-vision/Linux-FaceRecognition-FaceLivenessDetection/assets/153883841/b82f5c35-09d0-4064-a252-4bcd14e22407"/>
</a><br/><br/>

<p align="center">
    <img alt="" src="https://recognito.vision/wp-content/uploads/2024/03/NIST.png" width=90%/>
</p>
<p align="center" style="font-size: 24px; font-weight: bold;">
    <a href="https://pages.nist.gov/frvt/html/frvt11.html" target="_blank">
        Latest NIST FRVT Report
    </a>  
</p>

# On-Premise Face Recognition, Liveness Detection, Face Attribute Analysis SDK Demo (Windows Server)
Welcome to our Face SDK Demos repository! Here you will find demos showcasing the capabilities of our on-premise Face SDKs, including face recognition, liveness detection, and face attribute analysis. Our SDK is designed to work seamlessly on **Windows** Server platforms and can be integrated into various systems such as **eKYC** solutions and **CCTV** systems.

Our [**Product List**](https://github.com/recognito-vision/Product-List/) for ID verification.

## <img src="https://github.com/recognito-vision/.github/assets/153883841/dc7c1c3f-8269-475c-a689-cb57be36a920" alt="home" width="25">   RECOGNITO Product Documentation
&emsp;&emsp;<a href="https://docs.recognito.vision" style="display: flex; align-items: center;"><img src="https://recognito.vision/wp-content/uploads/2024/05/book.png" style="width: 64px; margin-right: 5px;"/></a>

## <img src="https://github.com/recognito-vision/Linux-FaceRecognition-FaceLivenessDetection/assets/153883841/d0991c83-44f0-4d38-bcc8-74376ce93ded" alt="feature" width="25">  Features
- **Face Recognition:** Identify and verify individuals by comparing their facial features.
- **Liveness Detection:** Determine whether a face is live or spoofed to prevent fraud in authentication processes.
- **Face Attribute Analysis:** Extract facial attributes such as age, gender and more from facial images for demographic analysis.

## <img src="https://github.com/recognito-vision/Linux-FaceRecognition-FaceLivenessDetection/assets/153883841/c15b7c1d-346f-4b0b-ad1e-c65882b14d27" alt="face recognition, liveness detection SDK demo description" width="25">  Windows Face SDK Demo Description
  | No.      | Demo | Description |
  |:------------------:|------------------|------------------|
  | 1        | [Flask Demo](https://github.com/recognito-vision/Windows-FaceRecognition-FaceLivenessDetection/tree/main/flask)    | Flask Server Demo for 1:1 verification, liveness detection |
  | 2        | [Gradio Demo](https://github.com/recognito-vision/Windows-FaceRecognition-FaceLivenessDetection/tree/main/gradio)    | Gradio UI Demo for 1:1 verification, liveness detection |
  | 3        | [Video Surveillance Demo](https://github.com/recognito-vision/Windows-FaceRecognition-FaceLivenessDetection/tree/main/video_surveillance_demo)    | Video Surveillance Demo for 1:N identification |

## <img src="https://github.com/recognito-vision/Face-SDK-Windows-Demo/assets/153883841/8a641c1e-cd1b-4336-9bad-ceffd580daaf" alt="system" width="25">  System Requirements
 - **Windows System:** Windows 10 or later
 - **CPU:** 8 cores
 - **RAM:** 8 GB
 - **HDD:** 8 GB

## <img src="https://github.com/recognito-vision/Linux-FaceRecognition-FaceLivenessDetection/assets/153883841/cd7a78b3-78da-4bd0-b12d-11771ab7345b" alt="install" width="25">  Installation

1. Clone this repository to your local machine:

    ```
    git clone https://github.com/recognito-vision/Windows-FaceRecognition-FaceLivenessDetection.git
    ```
   Download `engine` folder from [Here](https://drive.google.com/file/d/1GkpMJjMYCwtGpdtuYX2LKYb8VkrlOJqs/view?usp=drive_link) and extract to `Windows-FaceRecognition-FaceLivenessDetection` folder.
   
2. Install `python-3.8.9.exe`,  `VC_redist.2013.exe`, `VC_redist.2015-2022.exe` files from `dependency` folder.

   **Important Note**: When install `python-3.8.9.exe`, have to tick the `Add Python3.8 to PATH` option.
   
      <img src="https://github.com/recognito-vision/Windows-FaceRecognition-FaceLivenessDetection/assets/153883841/97d5c639-3113-4e57-8a8d-2d9e69b02964" alt="Add Python3.8 to PATH" width="60%">
4. Install the Python package from the desired demo folder. (`flask`, `gradio`, `video_surveillance_demo`)
   ```
   cd Windows-FaceRecognition-FaceLivenessDetection\gradio
   python -m pip install -r requirements.txt
   ```
## <img src="https://github.com/recognito-vision/Linux-FaceRecognition-FaceLivenessDetection/assets/153883841/1c0d0786-c03f-42f2-9f9f-d9bf91778162" alt="install" width="25">  Setting Up SDK License Key  (Trial License Available)
- Run `app.py` from the demo folder.
     ```
     python app.py
     ```
- Get your HWID and share it with us
     
     ![HWID](https://github.com/recognito-vision/Windows-FaceRecognition-FaceLivenessDetection/assets/153883841/4e375399-e533-4913-be9d-260251d97a6b)
     
    <div style="display: flex; align-items: center;">
        <a target="_blank" href="mailto:hassan@recognito.vision"><img src="https://img.shields.io/badge/email-hassan@recognito.vision-blue.svg?logo=gmail " alt="www.recognito.vision"></a>
        &nbsp;&nbsp;&nbsp;&nbsp;<a target="_blank" href="https://wa.me/+14158003112"><img src="https://img.shields.io/badge/whatsapp-+14158003112-blue.svg?logo=whatsapp " alt="www.recognito.vision"></a>
        &nbsp;&nbsp;&nbsp;&nbsp;<a target="_blank" href="https://t.me/recognito_vision"><img src="https://img.shields.io/badge/telegram-@recognito__vision-blue.svg?logo=telegram " alt="www.recognito.vision"></a>
        &nbsp;&nbsp;&nbsp;&nbsp;<a target="_blank" href="https://join.slack.com/t/recognito-workspace/shared_invite/zt-2d4kscqgn-"><img src="https://img.shields.io/badge/slack-recognito__workspace-blue.svg?logo=slack " alt="www.recognito.vision"></a>
    </div>
- Copy the `license.txt` license file to the `engine` folder.
     
     ![license](https://github.com/recognito-vision/Windows-FaceRecognition-FaceLivenessDetection/assets/153883841/0f774bb6-1233-40cc-bfdd-84cd06554c12)

## <img src="https://github.com/recognito-vision/Linux-FaceRecognition-FaceLivenessDetection/assets/153883841/7ed1f28b-bb29-4c83-809c-015e2f8e38ad" alt="install" width="25">  Running Demo
- Run `app.py` from the desired demo folder. (`flask`, `gradio`, `video_surveillance_demo`)
     ```
     python app.py
     ```
   ![run](https://github.com/recognito-vision/Windows-FaceRecognition-FaceLivenessDetection/assets/153883841/b4a3d8eb-2870-4683-847e-f972fb79968e)

- **Video Surveillance Demo**

  Test Photo Match (photo vs photo face identification), Video Surveillance (photo vs video face identification).
  
  Media files, RTSP, web camera can be used as input video.

  <p align="center">
      <img src="https://github.com/recognito-vision/Windows-FaceRecognition-FaceLivenessDetection/assets/153883841/d36da9cc-0124-4d1b-814b-c18e8809f8ea" width="45%" />
      <img src="https://github.com/recognito-vision/Windows-FaceRecognition-FaceLivenessDetection/assets/153883841/4428f788-d641-4fed-9b6f-901212d1d454" width="45%" />
  </p>
  <p align="center">
      <img src="https://github.com/recognito-vision/Windows-FaceRecognition-FaceLivenessDetection/assets/153883841/093af24f-e95a-4cca-84e3-18d89661e549" width="45%" />
      <img src="https://github.com/recognito-vision/Windows-FaceRecognition-FaceLivenessDetection/assets/153883841/47065f6e-9971-41a3-a0cf-dfae9e8e3cf9" width="45%" />
  </p>
  <p align="center">
      <img src="https://github.com/recognito-vision/Windows-FaceRecognition-FaceLivenessDetection/assets/153883841/0a257855-5e35-4e6a-8a96-e646f8be6c19" width="45%" />
      <img src="https://github.com/recognito-vision/Windows-FaceRecognition-FaceLivenessDetection/assets/153883841/e51856ab-0f5a-4da1-9fe2-ba8efa04a0d9" width="45%" />
  </p>
- **Flask Demo**

  To test the API, you can use [Postman](https://www.postman.com/downloads/). Here are the endpoints for testing
  
    - `http://{xx.xx.xx.xx}:8000/api/compare_face`
    - `http://{xx.xx.xx.xx}:8000/api/analyze_face`

    <img src="https://github.com/recognito-vision/Linux-FaceRecognition-FaceLivenessDetection/assets/153883841/3e078019-b760-4798-a058-d61165fd78af" alt="lite-recognition-flask" width="90%"><br/>
    <img src="https://github.com/recognito-vision/Linux-FaceRecognition-FaceLivenessDetection/assets/153883841/c5d54556-7c55-4a18-b9f9-cf3b21e2f1e8" alt="lite-liveness-flask" width="90%">

- **Gradio:**
  
    Go to [http://127.0.0.1:7860/](http://127.0.0.1:7860/) on a web browser.
  
    <img src="https://github.com/recognito-vision/Linux-FaceRecognition-FaceLivenessDetection/assets/153883841/dab63403-0d9d-45f9-810c-810c22e4ad8d" alt="lite-recognition-gradio" width="90%">

    <img src="https://github.com/recognito-vision/Linux-FaceRecognition-FaceLivenessDetection/assets/153883841/6f5c117b-1d5c-4ad9-8980-c1eb26fc6d25" alt="lite-liveness-gradio" width="90%">
    
## <img src="https://github.com/recognito-vision/Linux-FaceRecognition-FaceLivenessDetection/assets/153883841/78c5efee-15f3-4406-ab4d-13fd1182d20c" alt="contact" width="25">  Support
For any questions, issues, or feature requests, please contact our support team.

<div style="display: flex; align-items: center;">
    <a target="_blank" href="mailto:hassan@recognito.vision"><img src="https://img.shields.io/badge/email-hassan@recognito.vision-blue.svg?logo=gmail " alt="www.recognito.vision"></a>
    &nbsp;&nbsp;&nbsp;&nbsp;<a target="_blank" href="https://wa.me/+14158003112"><img src="https://img.shields.io/badge/whatsapp-+14158003112-blue.svg?logo=whatsapp " alt="www.recognito.vision"></a>
    &nbsp;&nbsp;&nbsp;&nbsp;<a target="_blank" href="https://t.me/recognito_vision"><img src="https://img.shields.io/badge/telegram-@recognito__vision-blue.svg?logo=telegram " alt="www.recognito.vision"></a>
    &nbsp;&nbsp;&nbsp;&nbsp;<a target="_blank" href="https://join.slack.com/t/recognito-workspace/shared_invite/zt-2d4kscqgn-"><img src="https://img.shields.io/badge/slack-recognito__workspace-blue.svg?logo=slack " alt="www.recognito.vision"></a>
</div>
<br/>
<p align="center">
    &emsp;&emsp;<a href="https://recognito.vision" style="display: flex; align-items: center;"><img src="https://recognito.vision/wp-content/uploads/2024/03/recognito_64_cl.png" style="width: 32px; margin-right: 5px;"/></a>
    &nbsp;&nbsp;&nbsp;&nbsp;<a href="https://www.linkedin.com/company/recognito-vision" style="display: flex; align-items: center;"><img src="https://recognito.vision/wp-content/uploads/2024/03/linkedin_64_cl.png" style="width: 32px; margin-right: 5px;"/></a>
    &nbsp;&nbsp;&nbsp;&nbsp;<a href="https://huggingface.co/recognito" style="display: flex; align-items: center;"><img src="https://recognito.vision/wp-content/uploads/2024/03/hf_64_cl.png" style="width: 32px; margin-right: 5px;"/></a>
    &nbsp;&nbsp;&nbsp;&nbsp;<a href="https://github.com/recognito-vision" style="display: flex; align-items: center;"><img src="https://recognito.vision/wp-content/uploads/2024/03/github_64_cl.png" style="width: 32px; margin-right: 5px;"/></a>
    &nbsp;&nbsp;&nbsp;&nbsp;<a href="https://hub.docker.com/u/recognito" style="display: flex; align-items: center;"><img src="https://recognito.vision/wp-content/uploads/2024/03/docker_64_cl.png" style="width: 32px; margin-right: 5px;"/></a>
    &nbsp;&nbsp;&nbsp;&nbsp;<a href="https://www.youtube.com/@recognito-vision" style="display: flex; align-items: center;"><img src="https://recognito.vision/wp-content/uploads/2024/04/youtube_64_cl.png" style="width: 32px; margin-right: 5px;"/></a>
</p>
