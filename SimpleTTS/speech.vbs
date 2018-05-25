Set args = WScript.Arguments
Set spV=CreateObject("sapi.spvoice") 

volume=args(0)
rate=args(1)
voice=args(2)
message=args(3) 

Set spV.voice = spV.GetVoices.Item(voice)
spV.Volume = volume
spV.Rate = rate

spV.Speak message