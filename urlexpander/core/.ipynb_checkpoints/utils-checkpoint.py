def chunks(iterable, chunksize):
    """Yield successive n-sized chunks from l.
    
    :input iterable: an iterable
    :input chunksize: chunksize
    """
    for i in range(0, len(iterable), chunksize):
        yield iterable[i:i + chunksize]