
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
from colorama import Fore,Style
from sources import*



def generate_exchange(sources,allowable_tolerance_in_average,debug_mode):


    data_frames = []
        

    for url_and_parameter in sources:
            
        r = requests.get(url_and_parameter[1])
        datos = r.text
        soup = BeautifulSoup(datos,"lxml")
        soup = str(soup)

        keyword_position = soup.find(url_and_parameter[2])
        value = soup [keyword_position+url_and_parameter[3] : keyword_position + url_and_parameter[4]]

        

            

        if "," in value:

            try:
                value = float(value.replace(",","."))
                data_frames.append([
                    url_and_parameter[0],                   #0
                    url_and_parameter[1],                   #1
                    url_and_parameter[2],                   #2
                    url_and_parameter[3],                   #3
                    url_and_parameter[4],                   #4
                    keyword_position,                       #5
                    float(value),                           #6
                    None                                    #7
                    ])

            except ValueError:            
                data_frames.append([
                    url_and_parameter[0],                   #0
                    url_and_parameter[1],                   #1
                    url_and_parameter[2],                   #2
                    url_and_parameter[3],                   #3
                    url_and_parameter[4],                   #4
                    keyword_position,                       #5
                    value,                                  #6
                    "url broken"                            #7
                    ])



        elif "." in value:

            try:                
                data_frames.append([
                    url_and_parameter[0],                   #0
                    url_and_parameter[1],                   #1
                    url_and_parameter[2],                   #2
                    url_and_parameter[3],                   #3
                    url_and_parameter[4],                   #4
                    keyword_position,                       #5
                    float(value),                           #6
                    None                                    #7
                    ])

            except ValueError:
                data_frames.append([
                    url_and_parameter[0],                   #0
                    url_and_parameter[1],                   #1
                    url_and_parameter[2],                   #2
                    url_and_parameter[3],                   #3
                    url_and_parameter[4],                   #4
                    keyword_position,                       #5
                    value,                                  #6
                    "url broken"                            #7
                    ])

        else:
            data_frames.append([
                    url_and_parameter[0],                   #0
                    url_and_parameter[1],                   #1
                    url_and_parameter[2],                   #2
                    url_and_parameter[3],                   #3
                    url_and_parameter[4],                   #4
                    keyword_position,                       #5
                    value,                                  #6
                    "url broken"                            #7
                    ])
    

        

    


    sum_of_values=0.
    num_of_values=0

    for data_frame in data_frames:
        if data_frame[7] == None:
            num_of_values += 1
            sum_of_values += data_frame[6]
            

    provisional_average = sum_of_values/num_of_values

    out_of_tolerance = provisional_average * allowable_tolerance_in_average



    data_frames_in_average = []

    for data_frame in data_frames:
        if data_frame[7] == None:
            if ((provisional_average - out_of_tolerance) > data_frame[6]) or ((provisional_average + out_of_tolerance) < data_frame[6]):
                data_frames_in_average.append([
                    data_frame[0],                   #0
                    data_frame[1],                   #1
                    data_frame[2],                   #2
                    data_frame[3],                   #3
                    data_frame[4],                   #4
                    data_frame[5],                   #5
                    data_frame[6],                   #6
                    "out of average"                 #7
                    ])

            else:
                data_frames_in_average.append(data_frame)
        else:
            data_frames_in_average.append(data_frame)

            
    
    sum_of_values=0.
    num_of_values=0

    for data_frame in data_frames_in_average:
        if data_frame[7] == None:
            num_of_values += 1
            sum_of_values += data_frame[6]
            

    average = sum_of_values/num_of_values

    

            
    if debug_mode:

        print ("\n\n____________________________________________RUNNING THE TEST___________________________________________")

        for data_frame in data_frames_in_average:
            
            if data_frame[7] == "url broken":
                print ("\n" +  f"{Fore.RED}The source: {Style.RESET_ALL}" + str(data_frame[0]) + " " + str(data_frame[1]) + f"{Fore.RED} is broken, please, check out the parameters of data position. \n {Style.RESET_ALL}" +     f"{Fore.BLUE}In this position: {Style.RESET_ALL}" + str(data_frame[5]) + f"{Fore.BLUE} there are these data in the parameter range: \n\n{Style.RESET_ALL}" + data_frame[6] + "\n")

            elif data_frame[7] == "out of average":
                print ("\n" +  f"{Fore.RED}The source: {Style.RESET_ALL}" + str(data_frame[0]) + " " + str(data_frame[1]) + f"{Fore.RED} is out of tolerance, the value: {Style.RESET_ALL}" + str(data_frame[6]) + f"{Fore.RED} ​​are to far of the average, the average is: {Style.RESET_ALL}" + str(provisional_average) + f"{Fore.RED} (adjust allowed average parameter or delete this source). {Style.RESET_ALL}" + "\n")

            elif data_frame[7] == None:
                print("\n" +  f"{Fore.GREEN}The source: {Style.RESET_ALL}" + str(data_frame[0]) + " " + str(data_frame[1]) + f"{Fore.GREEN} is OK {Style.RESET_ALL} \n")
        
        print("\n" + str(datetime.now())) 
        print ("____________________________________________END OF THE TEST___________________________________________\n\n")
    



    return average




while 1:

    USD_to_EUR = (generate_exchange(USDtoEUR,0.05,True))
    USD_to_GBP = (generate_exchange(USDtoGBP,0.05,True))


    print(USD_to_EUR,USD_to_GBP)
    time.sleep(60)


