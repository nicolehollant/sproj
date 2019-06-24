#!/bin/bash

# Some script to prove something to myself
# TODO: fix trailing commas, and clean up 


# helper function to get synonyms and antonyms
getSyns(){
    # get the line number of this section
    partOfSpeechInd=${1%:*}
    partOfSpeechInd=$((partOfSpeechInd + 1))
    # get the line number of the next section
    nextSection=`tail -n +$partOfSpeechInd temp | grep -n "### " | head -n 1`
    nextSection=${nextSection%:*}
    # if the next section exists
    if ! [ -z "$nextSection" ]
    then
        # extract relavent lines
        partOfSpeechLines=`sed -n $partOfSpeechInd,$((partOfSpeechInd + nextSection - 2))p temp`
        antonyms=`echo "$partOfSpeechLines" | grep -n "@@@ antonyms"`
        # check for antonyms
        if ! [ -z "$antonyms" ]
        then
            antonyms=$((${antonyms%:*}))
            if [ $antonyms -lt $nextSection ] # antonyms belong to this section
            then
                # find next subsection
                nextSubsection=`echo "$partOfSpeechLines" | sed ${antonyms}d | grep -n "@@@ " | head -n 1`
                nextSubsection=$((${nextSubsection%:*}))
                if [ $nextSubsection -lt $nextSection ] # if the next subsection occurs before the next section
                then
                    if [ $nextSubsection -ne 0 ] # if the next subsection exists
                    then
                        # extract the antonyms and synonyms
                        antonymsSection=`echo "$partOfSpeechLines" | sed -n ${antonyms},${nextSubsection}p`
                        synonymsSection=`echo "$partOfSpeechLines" | sed ${antonyms},${nextSubsection}d`
                    else 
                        # extract the antonyms and synonyms
                        antonymsSection=`echo "$partOfSpeechLines" | sed -n ${antonyms},${nextSection}p`
                        synonymsSection=`echo "$partOfSpeechLines" | sed ${antonyms},${nextSection}d`
                    fi
                else
                    # extract the antonyms and synonyms
                    antonymsSection=`echo "$partOfSpeechLines" | sed -n ${antonyms},${nextSection}p`
                    synonymsSection=`echo "$partOfSpeechLines" | sed ${antonyms},${nextSection}d`
                fi
                # do some string processing and save to a file
                echo "$synonymsSection" > adjSynonyms
                while read adjSynonyms ; do echo ${adjSynonyms} | cut -f1 -d"(" | cut -f1 -d"@"; done < adjSynonyms > adjSynonyms2 ; mv adjSynonyms2 adjSynonyms
                awk 'NF' adjSynonyms | cut -c 4- | rev | cut -c2- | sed 's/$/"/' | rev | sed 's/$/",/' > adjSynonyms2
                mv adjSynonyms2 adjSynonyms

                echo "$antonymsSection" > adjAntonyms
                while read adjAntonyms ; do echo ${adjAntonyms} | cut -f1 -d"(" | cut -f1 -d"@"; done < adjAntonyms > adjAntonyms2 ; mv adjAntonyms2 adjAntonyms
                awk 'NF' adjAntonyms | cut -c 4- | rev | cut -c2- | sed 's/$/"/' | rev | sed 's/$/",/' > adjAntonyms2
                mv adjAntonyms2 adjAntonyms

                synonyms=`cat adjSynonyms`
                antonyms=`cat adjAntonyms`
            fi
        else
            echo "$partOfSpeechLines" > adjSynonyms
            while read adjSynonyms ; do echo ${adjSynonyms} | cut -f1 -d"(" | cut -f1 -d"@"; done < adjSynonyms > adjSynonyms2 ; mv adjSynonyms2 adjSynonyms
            awk 'NF' adjSynonyms | cut -c 4- | rev | cut -c2- | sed 's/$/"/' | rev | sed 's/$/",/' > adjSynonyms2
            mv adjSynonyms2 adjSynonyms
            synonyms=`cat adjSynonyms`
            antonyms=""
        fi
        # pipe synonyms and antonyms to file
        echo \"$2\": {\"synonyms\": [$synonyms], \"antonyms\": [$antonyms]}, >> response.json
    else
        echo "next section DNE"
    fi
}

echo { > response.json

# loop over some list of words
for word in well pretty cool love
do
# get the page and convert it to markdown
curl -G https://words.bighugelabs.com/$word | pandoc -f html -t markdown -s -o temp

# replace #### with @@@
while read temp ; do echo ${temp//####\ /@@@\ } ; done < temp > temp2 ; mv temp2 temp
echo \"$word\": { >> response.json

# check for existence of categories and get their synonyms
adjective=`cat temp | grep -n "### adjective"`
adverb=`cat temp | grep -n "### adverb"`
noun=`cat temp | grep -n "### noun"`
verb=`cat temp | grep -n "### verb"`
if ! [ -z "$adjective" ]
then
    echo "adjective synonyms exist"
    getSyns $adjective adjective
fi

if ! [ -z "$adverb" ]
then
    echo "adverb synonyms exist"
    getSyns $adverb adverb
fi

if ! [ -z "$noun" ]
then
    echo "noun synonyms exist"
    getSyns $noun noun
fi

if ! [ -z "$verb" ]
then
    echo "verb synonyms exist"
    getSyns $verb verb
fi

echo }, >> response.json
done
echo } >> response.json
