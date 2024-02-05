class GenerateVideo:
    def __init__(self, topic):
        self.topic = topic  

    def start(self):

        data = {
            1: {
                "text": "Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen.",
                "video": "https://media.gettyimages.com/id/99150399/video/carbon-capture-photosynthesis.mp4?b=1&s=mp4-640x640-gi&k=20&c=EwPF8P4OFKVdGyLEpXD2EqaG1IPRsmEzWTVkp_sax08=",
                "audio": "/static/audio/1.mp3",
            },
            2: {
                "text": "During photosynthesis, plants use chlorophyll to capture sunlight energy in their leaves.",
                "video": "https://media.gettyimages.com/id/1716353913/video/plants-producing-water-through-sunlight.mp4?b=1&s=mp4-640x640-gi&k=20&c=s_MlVDzonWxdbeuGzEm4chRhjMIOJE_oiXaxLFINgOs=",
                "audio": "/static/audio/2.mp3",
            },
            3: {
                "text": "The captured energy is used to power the conversion of carbon dioxide and water into glucose.",
                "video": "https://media.gettyimages.com/id/1392688888/video/hydrogen-molecule-we-move-to-the-molecular-level-and-fly-up-to-the-hydrogen-molecule-the.mp4?b=1&s=mp4-640x640-gi&k=20&c=cEPU41cg_YFrDFh41J-Exq7e7G0kkbmunxqXlBw5q9E=",
                "audio": "/static/audio/3.mp3",
            },
            4: {
                "text": "Glucose is a sugar that serves as a source of energy for plants.",
                "video": "https://pixabay.com/get/ge7a0d0b7ccc221e100e5fb6ecf52d8dc3f09fc1b77bb16f504e2c17f0cff30890fb34e793ce6d8cb94c465d897b4ba3296d7612493e347ae2e66735c4c003146_640.jpg",
                "audio": "/static/audio/4.mp3",
            },
            5: {
                "text": "Oxygen is released as a byproduct of photosynthesis, which is crucial for the survival of most living organisms.",
                "video": "https://pixabay.com/get/g255ae457d8ea7773785e62458534c14298357c87c53e18ad053fe9de2b9177847fe82c79849e4edc473f233fc2e9e6d77c8a27e567c67b319a8e31ce4d0c1855_640.jpg",
                "audio": "/static/audio/5.mp3",
            },
            6: {
                "text": "Photosynthesis plays a vital role in maintaining the balance of oxygen and carbon dioxide in the atmosphere.",
                "video": "https://media.gettyimages.com/id/1336223810/video/carbon-neutral-carbon-dioxide-emitted-from-fossil-fuels-is-neutralized-with-renewable-energy.mp4?b=1&s=mp4-640x640-gi&k=20&c=EvKiNIMZ56iFil4s5kUYlZkYN3zwLUzkozThUZ-SNpc=",
                "audio": "/static/audio/6.mp3",
            },
        }

        return data 
    
if __name__ == "__main__":
    test = GenerateVideo("photosynthesis")
    print(test.start())