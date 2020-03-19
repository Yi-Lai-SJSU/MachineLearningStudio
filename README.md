# MachineLearningStudio


download and run：
docker-compose up --build --force-recreate

troubel-shooting：
https://forums.docker.com/t/denied-requested-access-to-the-resource-is-denied/49693/2
I have this problem.And resolve it now.
First, login your docker account.
Second, use this command:docker images,
this command can show you all images you have, then you chose an image to push.
Third, you should add a tag for image you chose. You can use this command:
docker tag existent_image_name:latest your_user_name/new_image_name:latest
Finally, you use this command:docker push your_user_name/new_image:latest
please try it again, if denied again.You can use sudo command like this:
sudo docker push your_user_name/new_image:latest
good luck!
