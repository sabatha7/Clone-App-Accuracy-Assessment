
# import os
# from azure.ai.vision.imageanalysis import ImageAnalysisClient
# from azure.ai.vision.imageanalysis.models import VisualFeatures
# from azure.core.credentials import AzureKeyCredential
# from matplotlib import pyplot as plt
# from PIL import Image, ImageDraw

# # Set the values of your computer vision endpoint and computer vision key
# # as environment variables:
# try:
#     endpoint = os.environ["VISION_ENDPOINT"]
#     key = os.environ["VISION_KEY"]
# except KeyError:
#     print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
#     print("Set them before running this sample.")
#     exit()

# # Create an Image Analysis client
# client = ImageAnalysisClient(
#     endpoint=endpoint,
#     credential=AzureKeyCredential(key)
# )

# # Get a caption for the image. This will be a synchronously (blocking) call.
# # result = client.analyze_from_url(
# #     image_url="https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png",
# #     visual_features=[VisualFeatures.CAPTION, VisualFeatures.READ],
# #     gender_neutral_caption=True,  # Optional (default is False)
# # )

# image_filename = 'Screenshot_20250103_212241_OKX.jpg'

# with open(image_filename, "rb") as image_fd:
#     image_data = image_fd.read()

# result = client.analyze(
#     image_data=image_data,
#     visual_features=[VisualFeatures.CAPTION, VisualFeatures.OBJECTS]
# )

# print("Image analysis results:")
# # Print caption results to the console
# print(" Caption:")
# if result.caption is not None:
#     print(f"   '{result.caption.text}', Confidence {result.caption.confidence:.4f}")

# # Get objects in the image
# if result.objects is not None:
#     print("\nObjects in image:")

#     # Prepare image for drawing
#     image = Image.open(image_filename)
#     fig = plt.figure(figsize=(image.width/100, image.height/100))
#     plt.axis('off')
#     draw = ImageDraw.Draw(image)
#     color = 'cyan'

#     for detected_object in result.objects.list:
#         # Print object name
#         print(" {} (confidence: {:.2f}%)".format(detected_object.tags[0].name, detected_object.tags[0].confidence * 100))
        
#         # Draw object bounding box
#         r = detected_object.bounding_box
#         bounding_box = ((r.x, r.y), (r.x + r.width, r.y + r.height)) 
#         draw.rectangle(bounding_box, outline=color, width=3)
#         plt.annotate(detected_object.tags[0].name,(r.x, r.y), backgroundcolor=color)

#     # Save annotated image
#     plt.imshow(image)
#     plt.tight_layout(pad=0)
#     outputfile = 'objects.jpg'
#     fig.savefig(outputfile)
#     print('  Results saved in', outputfile)

# Print text (OCR) analysis results to the console
# print(" Read:")
# if result.read is not None:
#     for line in result.read.blocks[0].lines:
#         print(f"   Line: '{line.text}', Bounding box {line.bounding_polygon}")
#         for word in line.words:
#             print(f"     Word: '{word.text}', Bounding polygon {word.bounding_polygon}, Confidence {word.confidence:.4f}")

# from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
# from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
# from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
# from msrest.authentication import ApiKeyCredentials
# import os, time, uuid

# # retrieve environment variables
# ENDPOINT = os.environ["VISION_PREDICTION_ENDPOINT"]
# # training_key = os.environ["VISION_TRAINING_KEY"]
# prediction_key = os.environ["VISION_PREDICTION_KEY"]
# prediction_resource_id = os.environ["VISION_PREDICTION_RESOURCE_ID"]

# # credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
# # trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
# # prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
# # predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

# publish_iteration_name = "Iteration2"

# project = {'id':'890587a1-ceb4-4e3f-b865-8658dcfd4267'}

# # Now there is a trained endpoint that can be used to make a prediction
# prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
# predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

# with open("examples/1736026817485.jpg", "rb") as image_contents:
#     results = predictor.classify_image(
#         project['id'], publish_iteration_name, image_contents.read())

#     # Display the results.
#     for prediction in results.predictions:
#         print("\t" + prediction.tag_name +
#               ": {0:.2f}%".format(prediction.probability * 100))
import os
import requests
import sys

# Define the endpoint and headers
ENDPOINT = os.environ["VISION_PREDICTION_ENDPOINT"]
url = ENDPOINT
prediction_key = os.environ["VISION_PREDICTION_KEY"]
headers = {
    "Prediction-Key": prediction_key,
    "Content-Type": "application/octet-stream"
}

# Read the image file and send it to the prediction URL
def analyze_image(image_path):
    """
    Analyzes an image by sending it to a specified URL and returns the probabilities of the top two predictions.
    Args:
        image_path (str): The file path to the image to be analyzed.
    Returns:
        str: A formatted string containing the probabilities of the top two predictions separated by a '|'.
        bool: Returns False if the request was not successful.
    Raises:
        None: This function does not raise any exceptions explicitly.
    """
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    # Make the request
    response = requests.post(url, headers=headers, data=image_data)

    # Check the response
    if response.status_code == 200:
        results = response.json()
        # for prediction in results['predictions']:print(f"{prediction['tagName']}: {prediction['probability'] * 100:.2f}%")
        winning = results['predictions'][0]
        won = results['predictions'][1]
        return "{}|{}".format(winning['probability'], won['probability'])
    else:
        pass
        # print(f"Error: {response.status_code}")
        # print(response.json())
    return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python app.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    result = analyze_image(image_path)
    print(result)
    