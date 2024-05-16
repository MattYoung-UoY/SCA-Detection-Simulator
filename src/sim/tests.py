
def sample_mean(dataset: list[int], sampleStart: int, sampleSize: int):
    if(len(dataset) == 0
       or sampleStart < 0
       or sampleStart > len(dataset)-1
       or sampleSize < 0
       or (sampleStart + sampleSize) > len(dataset)):
        raise ValueError('Parameters to sample_mean function incorrect!')
    
    samples = dataset[sampleStart:sampleStart+sampleSize]
    return sum(samples)/len(samples)
        