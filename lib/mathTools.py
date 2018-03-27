def clipText(text, width, font):
    lastChar = len(text)
    while font.size(text[:lastChar] if lastChar == len(text) else text[:lastChar].strip()+'...')[0]>width and lastChar > 0:
        lastChar-=1
    return text[:lastChar] if lastChar == len(text) else text[:lastChar].strip()+'...'
def clamp(val, minVal, maxVal):
    return max(min(val,maxVal),minVal)