echo "Creating virtual environment..."
echo
conda create -n Alana python=3.6 -y
eval "$(conda shell.bash hook)"
conda activate Alana

#echo -e "\nInstalling requirements for sample bot...\n"
#cd sample_bot && pip install -r requirements.txt

#cd ..
echo -e "\nInstalling requirements for grid libraries...\n"
cd grid_libraries && pip install -r requirements.txt

cd ..
echo -e "\nInstalling requirements for directions bot...\n"
cd directions_bot && pip install -r requirements.txt

cd ..
echo -e "\nInstalling requirements for events bot...\n"
cd events_bot && pip install -r requirements.txt

cd ..
echo -e "\nInstalling requirements for resource bot...\n"
cd resource_bot && pip install -r requirements.txt

#cd ..
#echo -e "\nInstalling requirements for persona bot...\n"
#cd persona_bot && pip install -r requirements.txt

#cd ..
#echo -e "\nInstalling requirements for coherence bot...\n"
#cd coherence_bot && pip install -r requirements.txt

cd ..
echo -e "\nInstalling supporting packages...\n"
cd utils && pip install -e .
