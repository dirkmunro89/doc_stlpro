echo $(docker ps -a -q) > existing.log
nri=$(cat existing.log | wc -w)
echo "Number of existing containers: "$nri
if [ "$nri" = "0" ]
then
    docker run --name stlpro --mount type=bind,source="$(pwd)"/srcs,target=/srcs -it stlpro 
elif [ "$nri" = "1" ]
then
    echo -n "Restarting and attaching to: "
    docker start  `docker ps -q -l` # restart it in the background
    docker attach `docker ps -q -l` # reattach the terminal & stdin
else
    docker stop $(docker ps -a -q)
    docker rm $(docker ps -a -q)
    docker run --name stlpro --mount type=bind,source="$(pwd)"/srcs,target=/srcs -it stlpro
fi

