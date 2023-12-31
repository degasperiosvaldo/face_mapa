
"""

    PROJECT: Face Mess Detection Web
    MADE BY: Mohd Ali Bin Naser
    GITHUB : github.com/mohdalibn

"""

# Importing the required libraries for the project
import streamlit as st
import mediapipe as mp
from PIL import Image
import numpy as np
import tempfile
import time
import cv2


# Sets the Streamlit App to Display in Wide Mode
st.set_page_config(layout="wide")

st.markdown(

    """
    
    <style>

        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');

        # font-face {
        # font-family: 'Poppins', san-serif;
        # font-style: normal;
        # font-weight: 400;
        
        # }

        html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        font-size: 20px;
        }

        # .css-16huue1{
        #     font-size: 24px;
        # }
        # .effi0qh0{
        #     font-size:20px;
        # }


    </style>

    """,

    unsafe_allow_html=True

)

# Adding the SideBar Markdown
st.markdown(
    """

    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{width:350px}

    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
        width:350px
        margin-left: -350px
        }

    </style>

    """,

    unsafe_allow_html=True,

)


# Setting the Title of the Streamlit App
# st.title("""Face Mesh Detection Web App osg""")
st.markdown("""<p style="font-size:50px;font-weight:500;">Detecção de malha facial</p>""",
            unsafe_allow_html=True)

st.markdown('---')

st.sidebar.title('Controles do aplicativo')  # Sidebar Title
# st.sidebar.subheader('parameters')  # Sidebar subheading


# This function is going to resize the User selected Image or Video File so that it fits within the assigned space in the Web App
@st.cache()
def FrameResize(Frame, FrameWidth=None, FrameHeight=None, InterpolationMtd=cv2.INTER_AREA):
    FrameDimensions = None
    height, width, _ = Frame.shape

    # We simply return the Image or Video Frame if both the Width and Height are None
    if FrameWidth is None and FrameHeight is None:
        return Frame

    # This statement executes if only the FrameWidth is None
    if FrameWidth is None:
        result = FrameWidth / float(width)
        FrameDimensions = (int(width * result), FrameHeight)

    else:
        result = FrameWidth / float(width)
        FrameDimensions = (FrameWidth, int(height * result))

    # Here, we resize the frame using the calculated values above using opencv
    ResizedFrame = cv2.resize(Frame, FrameDimensions,
                              interpolation=InterpolationMtd)

    # Return the new Resized Frame
    return ResizedFrame


# Creating a Streamlit Selectbox to give the user options to select a mode

SelectAppMode = st.sidebar.selectbox('Selecione um modo de aplicativo',
                                     ['Detalhes do aplicativo',
                                         'Imagem', 'Vídeo'],
                                     )

# Executing statements according to the User's choice
if SelectAppMode == 'Detalhes do aplicativo':

    # st.subheader('How To Use This App')
    st.markdown("""<p style="font-size: 32px; font-weight:500;color: #8B3DFF;">Como usar este aplicativo</p>""",
                unsafe_allow_html=True)

    st.markdown(

        """
        <p style="font-size: 20px;">
            Para começar, primeiro escolha um modo de aplicativo na barra lateral no lado esquerdo da página.
        </p>
        <p style="font-size: 20px;margin-bottom:2.5rem;">
            Existem dois modos disponíveis: Modo de imagem e Modo de vídeo .

        </p>
        <p style="font-size: 22px;color: #8B3DFF;">
            <b>Modo Imagem</b>.      
        </p>

        <p style="font-size: 20px;">
            No Modo Imagem, o usuário tem a opção de  <b> fazer upload de uma imagem</b>. Por padrão, o App já carrega uma <b>Imagem Demo</b>.
        </p>

        <p style="font-size: 20px;margin-bottom:2.5rem;">
            Na barra lateral o usuário tem a opção de controlar 4 <b>parâmetros </b> diferentes. A primeira é a opção de <b>selecionar o número de rostos a serem detectados na imagem</b>. That is followed by three sliders which gives the User the ability to adjust the <b>Detection Confidence</b>, <b>Mesh Thickness</b>, and <b>Mesh Circle Radius</b> respectively.
        </p>

        <p style="font-size: 22px;color: #8B3DFF;">
            <b>Modo vídeo</b>. 
        </p>

        <p style="font-size: 20px;">
            Under the Video Mode, the User has the option to  <b>Upload a Video</b> from their local machine. By default, the App already loads a <b>Demo Video</b>.
        </p>

        <p style="font-size: 20px;margin-bottom:2.5rem;">
            On the Sidebar, the User has the option to control 5 different <b>Parameters</b>. The first one is option to <b>Select the number of faces to detect in the Video</b>. That is followed by 4 sliders which gives the User the ability to adjust the <b>Detection Confidence</b>, <b>Tracking Confidence</b>,<b>Mesh Thickness</b>, and <b>Mesh Circle Radius</b> respectively.
        </p>


        """, unsafe_allow_html=True
    )

    st.markdown('---')

    # st.subheader('Como usar este aplicativo')
    st.markdown("""<p style="font-size: 32px; font-weight:500;color: #8B3DFF;">Important Note</p>""",
                unsafe_allow_html=True)

    st.markdown(

        """
        <p style="font-size: 20px;">
            The <b>processing of an Image or Video Frame using the Mediapipe library and OpenCV are entirely done on the computer's CPU</b>, and due this reason, the <b>Frame Rate (FPS) of the output vidoes are generally below 30 FPS</b>. 
        </p>

        """, unsafe_allow_html=True
    )

    # st.markdown(
    #     """

    #     <style>
    #     [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{width:350px}

    #     [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
    #         width:350px
    #         margin-left: -350px
    #         }
    #     </style>

    #     """,

    #     unsafe_allow_html=True,

    # )


# Variables created for ease of typing
MPDrawing = mp.solutions.drawing_utils
MPFaceMesh = mp.solutions.face_mesh

if SelectAppMode == 'Imagem':

    st.sidebar.markdown('---')

    st.markdown(
        """

        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{width:350px}

        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
            width:350px
            margin-left: -350px
            }
        </style>

        """,

        unsafe_allow_html=True,

    )

    # This allows Users to import an Image file from their local Machine
    UploadImageFile = st.sidebar.file_uploader(
        'Upload an Image', type=["png", "jpg", "jpeg"])

    # This statement executes when the file upload buffer is not empty
    if UploadImageFile is not None:
        ImageFile = np.array(Image.open(UploadImageFile))

        # These next 2 lines display the original image imported by the User on the Sidebar
        st.sidebar.text('Original Image Uploaded')
        st.sidebar.image(ImageFile)

    # If the User Upload file is empty, then we use a stock image
    else:
        StockDemoImg = "images/DemoImage1.jpg"
        ImageFile = np.array(Image.open(StockDemoImg))

        st.sidebar.text('Demo Image Provided')
        st.sidebar.image(ImageFile)

    st.sidebar.markdown('---')

    # This parameter is going to allow the User to input the number of faces that they want the model to detect on an Image or Video. We are setting the default number of faces to 2(value=2) and minimum to 1 (min_value=1)
    NumFaces = st.sidebar.number_input(
        'Select the number of faces you want to detect', value=2, min_value=1)

    st.sidebar.markdown('---')

    # Creates a Slider on the Sidebar for the User to set the Detection Confidence of the Model
    DetectionConfidence = st.sidebar.slider(
        'Minimum Detection Confidence', min_value=0.0, max_value=1.0, value=0.5)

    MeshThickness = st.sidebar.slider(
        'Mesh Drawing Thickness', min_value=1, max_value=10, value=2)

    MeshCircleRadius = st.sidebar.slider(
        'Mesh Draawing Circle Radius', min_value=1, max_value=10, value=1)

    DrawingSpec = MPDrawing.DrawingSpec(
        thickness=MeshThickness, circle_radius=MeshCircleRadius)

    FaceCount = 0
    Failed = False

    # The Code below is for the Statistics Dashboard
    with MPFaceMesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=NumFaces,
            min_detection_confidence=DetectionConfidence) as FaceMesh:

        MeshProcessResults = FaceMesh.process(ImageFile)
        OutputImage = ImageFile.copy()

        # This if statement is a fail check when the model isn't able to detect faces
        if MeshProcessResults.multi_face_landmarks is not None:

            Failed = False

            # Here is the code for drawing the Face Mesh Landmarks
            for FaceLandMarks in MeshProcessResults.multi_face_landmarks:

                # We increment our FaceCount Variable
                FaceCount += 1

                MPDrawing.draw_landmarks(
                    image=OutputImage,
                    landmark_list=FaceLandMarks,
                    connections=MPFaceMesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=DrawingSpec
                )

        else:
            Failed = True

        # Displaying the Resulting Output Image on the Main Page
        # st.subheader("Resulting Output Image")
        st.markdown(
            """<p style="font-size: 32px; font-weight:500;color: #8B3DFF;">Resulting Output Image</p>""", unsafe_allow_html=True)
        st.image(OutputImage, use_column_width=True)

        # st.subheader("**Detected Faces**")
        # st.markdown(
        #     """<p style="font-size: 32px; font-weight:500;">Detected Faces</p>""", unsafe_allow_html=True)

        FaceCountText, WidthText, HeightText = st.columns(3)

        ImageHeight, ImageWidth, _ = OutputImage.shape

        # This is for the FaceCount Value
        with FaceCountText:
            st.write(
                f"<h1 style='text-align:center;font-size:20px;'>Face Count</h1>", unsafe_allow_html=True)
            FCText = st.markdown("0")

        # This is for the Video Width Value
        with WidthText:
            st.write(
                f"<h1 style='text-align:center;font-size:20px;'>Image Width</h1>", unsafe_allow_html=True)
            WthText = st.write(
                f"<h1 style='text-align:center;color: #8B3DFF;'>{ImageWidth}</h1>", unsafe_allow_html=True)

        # This is for the Video Height Value
        with HeightText:
            st.write(
                f"<h1 style='text-align:center;font-size:20px;'>Image Height</h1>", unsafe_allow_html=True)
            HhtText = st.write(
                f"<h1 style='text-align:center;color: #8B3DFF;'>{ImageHeight}</h1>", unsafe_allow_html=True)

        # These if else statements display the right text accordingly
        if Failed:
            FCText.write(
                f"<h2 style='text-align:center;color: #8B3DFF;'>Sorry! The model is unable to detect faces. Please try using another image.</h2>", unsafe_allow_html=True)
        else:
            FCText.write(
                f"<h1 style='text-align:center;color: #8B3DFF;'>{FaceCount}</h1>", unsafe_allow_html=True)


if SelectAppMode == 'Vídeo':

    st.markdown(
        """<p style="font-size: 32px; font-weight:500;color: #8B3DFF;">Resulting Output Video</p>""", unsafe_allow_html=True)

    # This line suppress any deprecation warning that Streamlit may Output
    st.set_option('deprecation.showfileUploaderEncoding', False)

    # This lets the User Use their Webcam as direct input into the App
    UseWebcam = st.sidebar.button('Use Webcam')
    RecordOption = st.sidebar.checkbox('Record Video')

    if RecordOption:
        st.checkbox("Recording Video....", value=True)

    stFrame = st.empty()

    # This allows Users to import an Image file from their local Machine
    UploadVideoFile = st.sidebar.file_uploader(
        'Upload a Video', type=["mp4", "avi", "mov", "asf", "m4v"])

    TmpFile = tempfile.NamedTemporaryFile(delete=False)

    # This statement executes when the file upload buffer is not empty
    if not UploadVideoFile:

        # Executes if the User Clicks on the Webcam button
        if UseWebcam:
            CapVideo = cv2.VideoCapture(0)

        # If the User does use the webcam, then we use a stock video
        else:
            CapVideo = cv2.VideoCapture("videos/DemoVideo1.mp4")

    #
    else:
        TmpFile.write(UploadVideoFile.read())
        CapVideo = cv2.VideoCapture(TmpFile.name)

    # Getting the Video Width, Height, and FPS
    VideoWidth = int(CapVideo.get(cv2.CAP_PROP_FRAME_WIDTH))
    VideoHeight = int(CapVideo.get(cv2.CAP_PROP_FRAME_HEIGHT))
    VideoFPS = int(CapVideo.get(cv2.CAP_PROP_FPS))

    # If the Video Recording Option is selected by the User
    RecordingCodec = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')

    # Outputing the Recorded Video into a file
    OutputVideo = cv2.VideoWriter('recording1.mp4',
                                  RecordingCodec, VideoFPS, (VideoWidth, VideoHeight))

    # Displaying the video on the Sidebar
    st.sidebar.text("Demo Video")
    st.sidebar.video("videos/DemoVideo1.mp4")

    st.sidebar.markdown('---')

    st.markdown(
        """

        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{width:350px}

        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
            width:350px
            margin-left: -350px
            }
        </style>

        """,

        unsafe_allow_html=True,

    )

    # This parameter is going to allow the User to input the number of faces that they want the model to detect on an Image or Video. We are setting the default number of faces to 2(value=2) and minimum to 1 (min_value=1)
    NumFaces = st.sidebar.number_input(
        'Select the number of faces you want to detect', value=2, min_value=1)

    st.sidebar.markdown('---')

    # Creates a Slider on the Sidebar for the User to set the Detection Confidence of the Model
    DetectionConfidence = st.sidebar.slider(
        'Minimum Detection Confidence', min_value=0.0, max_value=1.0, value=0.5)

    TrackingConfidence = st.sidebar.slider(
        'Minimum Tracking Confidence', min_value=0.0, max_value=1.0, value=0.5)

    # st.sidebar.markdown('---')

    MeshThickness = st.sidebar.slider(
        'Mesh Drawing Thickness', min_value=1, max_value=10, value=2)

    MeshCircleRadius = st.sidebar.slider(
        'Mesh Draawing Circle Radius', min_value=1, max_value=10, value=1)

    DrawingSpec = MPDrawing.DrawingSpec(
        thickness=MeshThickness, circle_radius=MeshCircleRadius)

    FaceCountText, FPSText, WidthText, HeightText = st.columns(4)

    # This is for the FaceCount Value
    with FaceCountText:
        st.write(f"<h1 style='text-align:center;font-size:20px;'>Face Count</h1>",
                 unsafe_allow_html=True)
        FCText = st.markdown("0")

    # This is for the FPS Value
    with FPSText:
        st.write(f"<h1 style='text-align:center;font-size:20px;'>Frame Rate</h1>",
                 unsafe_allow_html=True)
        FPSText2 = st.markdown("0")

    # This is for the Video Width Value
    with WidthText:
        st.write(f"<h1 style='text-align:center;font-size:20px;'>Video Width</h1>",
                 unsafe_allow_html=True)
        WthText = st.markdown("0")

    # This is for the Video Height Value
    with HeightText:
        st.write(f"<h1 style='text-align:center;font-size:20px;'>Video Height</h1>",
                 unsafe_allow_html=True)
        HhtText = st.markdown("0")

    st.markdown('<hr/>', unsafe_allow_html=True)

    FaceCount = 0
    Failed = False
    FPS = 0
    FpsFrame = 0

    # The Code below is for the Statistics Dashboard
    with MPFaceMesh.FaceMesh(
            max_num_faces=NumFaces,
            min_detection_confidence=DetectionConfidence,
            min_tracking_confidence=TrackingConfidence) as FaceMesh:

        # Setting the PrevTime to calculate the FPS of the video
        PrevTime = 0

        while CapVideo.isOpened():
            FpsFrame += 1

            success, frame = CapVideo.read()

            if not success:
                continue

            MeshProcessResults = FaceMesh.process(frame)
            frame.flags.writeable = True

            FaceCount = 0

            # This if statement is a fail check when the model isn't able to detect faces
            if MeshProcessResults.multi_face_landmarks is not None:

                Failed = False

                # Here is the code for drawing the Face Mesh Landmarks
                for FaceLandMarks in MeshProcessResults.multi_face_landmarks:

                    # We increment our FaceCount Variable
                    FaceCount += 1

                    MPDrawing.draw_landmarks(
                        image=frame,
                        landmark_list=FaceLandMarks,
                        connections=MPFaceMesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=DrawingSpec,
                        connection_drawing_spec=DrawingSpec
                    )

            else:
                Failed = True

            # Calculating the FPS and Updating the PrevTime
            CurrTime = time.time()
            FPS = 1 // (CurrTime - PrevTime)
            PrevTime = CurrTime

            if RecordOption:
                OutputVideo.write(frame)

            FCText.write(
                f"<h2 style='text-align:center;color: #8B3DFF;'>{FaceCount}</h2>", unsafe_allow_html=True)

            FPSText2.write(
                f"<h2 style='text-align:center;color: #8B3DFF;'>{FPS}</h2>", unsafe_allow_html=True)

            WthText.write(
                f"<h2 style='text-align:center;color: #8B3DFF;'>{VideoWidth}</h2>", unsafe_allow_html=True)

            HhtText.write(
                f"<h2 style='text-align:center;color: #8B3DFF;'>{VideoHeight}</h2>", unsafe_allow_html=True)

            frame = cv2.resize(frame, (0, 0), fx=0.8, fy=0.8)
            frame = FrameResize(Frame=frame, FrameWidth=640)
            stFrame.image(frame, channels="BGR", use_column_width=True)
