#!/bin/bash
 
keys=1
depth=1
iterations=100
 
 # zero size
 curl -X POST localhost:8080/runLambda/tcp_resp -d "{\"name\": \"Alice\", \"value_len\": 0}"
 curl -X POST localhost:8081/runLambda/tcp_call -d "{\"name\": \"Alice\", \"value_len\": 0}"
 #curl -X POST localhost:8081/runLambda/req_cache_caller -d "{\"name\": \"Alice\", \"value_len\": 0}"
 #curl -X POST localhost:8081/runLambda/curl_cache_caller -d "{\"name\": \"Alice\", \"value_len\": 0}"
 #curl -X POST localhost:8080/runLambda/ipc_resp -d '{"num_keys":"1", "depth" : "1", "value_len" : "0"}' & # setup resp
 #curl -X POST localhost:8081/runLambda/ipc_call -d '{"num_keys":"1", "depth" : "1", "value_len" : "0"}'
 
 
 for (( length=64; length<700000; length*=4 )) 
 do 
      echo $length;
     curl -X POST localhost:8080/runLambda/tcp_resp -d "{\"name\": \"Alice\", \"value_len\": $length}"
     curl -X POST localhost:8081/runLambda/tcp_call -d "{\"name\": \"Alice\", \"value_len\": $length}"
     #curl -X POST localhost:8081/runLambda/req_cache_caller -d "{\"name\": \"Alice\", \"value_len\": $length}"
     #curl -X POST localhost:8081/runLambda/curl_cache_caller -d "{\"name\": \"Alice\", \"value_len\": $length}"
     #curl -X POST localhost:8080/runLambda/ipc_resp -d '{"num_keys":"1", "depth" : "1", "value_len" : $length}' & # setup resp
     #curl -X POST localhost:8081/runLambda/ipc_call -d '{"num_keys":"1", "depth" : "1", "value_len" : $length}'
 done


