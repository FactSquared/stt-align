import json
import sttalign
import os
import requests
import argparse

#proofread_id = 'd361252d-2eb2-4998-b608-1e4872b562c2'

def main(proofread_id):
    proofread_call = requests.get(f'https://stella-api.prod.factsquared.com/transcripts/{proofread_id}')
    proofread = proofread_call.json()['data']

    firstdraft_id = proofread['metadata']['firstdraft_id']
    firstdraft_call = requests.get(f'https://stella-api.prod.factsquared.com/transcripts/{firstdraft_id}')
    firstdraft = firstdraft_call.json()['data']['text_list']

    transcript = []
    for words in proofread['text_list']:
        transcript.append(words['text'])
    transcript = ''.join(transcript)

    stt = {"words": []}

    # Divide evenly
    for i in range(len(firstdraft)):
        seq = firstdraft[i]
        total_time = seq['end_time'] - seq['start_time']
        words = seq['text'].split(' ')

        tpw = total_time / len(words) # time per word

        for j in range(len(words)):
            stt['words'].append({
                "word": words[j],
                "start": seq['start_time'] + j * tpw,
                "end": seq['start_time'] + (j+1) * tpw,
            })

    # Put together
    os.system('mkdir -p tmp/')
    stt_file = f'tmp/stt_{proofread_id}.json'
    with open(stt_file, 'w') as f:
        json.dump(stt, f, indent=4)

    # Run stt align
    aligned = sttalign.alignJSONText(stt_file, transcript)
    os.system('mkdir -p out/')
    with open(f'out/aligned_{proofread_id}.json', 'w') as f:
        json.dump(aligned, f, indent=4)


parser = argparse.ArgumentParser('align word timings with known transcript')
parser.add_argument('proofread_id', help='The STELLA transcript id for the proofread transcript')
args = parser.parse_args()

proofread_id = args.proofread_id

main(proofread_id)

