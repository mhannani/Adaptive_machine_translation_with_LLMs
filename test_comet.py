# from comet import download_model, load_from_checkpoint
# model_path = download_model("Unbabel/wmt22-comet-da")
# model = load_from_checkpoint(model_path)
# data = [
#     {
#         "src": "Dem Feuer konnte Einhalt geboten werden",
#         "mt": "The fire could be stopped",
#         "ref": "They were able to control the fire."
#     },
#     {
#         "src": "Schulen und Kindergärten wurden eröffnet.",
#         "mt": "Schools and kindergartens were open",
#         "ref": "Schools and kindergartens opened"
#     }
# ]
# model_output = model.predict(data, batch_size=8, gpus=1)
# print (model_output)