import json

def get_transcript(data):
    #f = open('file.json')

    #data = json.load(f)

    speakers = {}

    for elem in data['speaker_labels']:
        speakers[elem['speaker']] = 1

    speakers = speakers.keys()

    results = data['results']

    results_agg = []

    # count tokens :
    tokens = 0

    for result in results:
        dic = {}
        ts = result['alternatives'][0]['timestamps']
        tokens = tokens + len(ts)
        begin = ts[0][1]
        end = ts[-1][2]
        transcript = result['alternatives'][0]['transcript']
        
        dic['begin'] = begin
        dic['end'] = end
        dic['transcript'] = transcript
        dic['speaker'] = 0
        
        results_agg.append(dic)

    idx = {}
    for elem in data['speaker_labels']:
        idx[elem['from']] = elem['speaker']

    for result in results_agg:
        result['speaker'] = idx[result['begin']]
       
    return results_agg
