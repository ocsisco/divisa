
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from colorama import Fore,Style
from sources import*



def generate_exchange(sources,allowable_tolerance_in_average,debug_mode):


    ID='ID'
    URL='URL'
    KEYWORD='KEYWORD'
    INIT='INIT'
    END='END'
    KEYWORD_POSITION='KEYWORD_POSITION'
    VALUE='VALUE'
    DIAGNOSIS='DIAGNOSIS'

    URL_BROKEN='url broken'
    OUT_OF_AVERAGE='out of average'





    data_frames = []
        

    for source in sources:

        source_dic = {
        ID                : source[0],
        URL               : source[1],
        KEYWORD           : source[2],
        INIT              : source[3],
        END               : source[4],
        KEYWORD_POSITION  : None,
        VALUE             : None,
        DIAGNOSIS         : None
        }




            
        r = requests.get(source_dic[URL])
        datos = r.text
        soup = BeautifulSoup(datos,"lxml")
        soup = str(soup)

        keyword_position = soup.find(source_dic[KEYWORD])
        value = soup [keyword_position+source_dic[INIT] : keyword_position + source_dic[END]]

        source_dic.update({KEYWORD_POSITION : keyword_position})

            

        if "," in value:

            try:
                value = float(value.replace(",","."))
                source_dic.update({
                    VALUE : float(value),
                    DIAGNOSIS : None 
                    })

            except ValueError:
                source_dic.update({
                    VALUE : value,
                    DIAGNOSIS : URL_BROKEN
                    })            


        elif "." in value:

            try:                
                source_dic.update({
                    VALUE : float(value),
                    DIAGNOSIS : None
                })

            except ValueError:
                source_dic.update({
                    VALUE : value,
                    DIAGNOSIS : URL_BROKEN
                })

        else:
            source_dic.update({
                VALUE : value,
                DIAGNOSIS : URL_BROKEN
            })
        
        data_frames.append(source_dic)
    

    


    sum_of_values=0.
    num_of_values=0

    for source_dic in data_frames:
        if source_dic[DIAGNOSIS] == None:
            num_of_values += 1
            sum_of_values += source_dic[VALUE]
            

    provisional_average = sum_of_values/num_of_values

    out_of_tolerance = provisional_average * allowable_tolerance_in_average



    data_frames_in_average = []

    for source_dic in data_frames:
        if source_dic[DIAGNOSIS] == None:

            if ((provisional_average - out_of_tolerance) > source_dic[VALUE]) or ((provisional_average + out_of_tolerance) < source_dic[VALUE]):
                
                source_dic.update({
                    DIAGNOSIS : OUT_OF_AVERAGE
                    })
                data_frames_in_average.append(source_dic)

            else:
                data_frames_in_average.append(source_dic)
        else:
            data_frames_in_average.append(source_dic)

            
    
    sum_of_values=0.
    num_of_values=0

    for source_dic in data_frames_in_average:
        if source_dic[DIAGNOSIS] == None:
            num_of_values += 1
            sum_of_values += source_dic[VALUE]
            

    average = sum_of_values/num_of_values

    

            
    if debug_mode:

        print ("\n\n____________________________________________RUNNING THE TEST___________________________________________")

        for source_dic in data_frames_in_average:
            
            if source_dic[DIAGNOSIS] == URL_BROKEN:
                print ("\n" +  f"{Fore.RED}The source: {Style.RESET_ALL}" + str(source_dic[ID]) + " " + str(source_dic[URL]) + f"{Fore.RED} is broken, please, check out the parameters of data position. \n {Style.RESET_ALL}" +     f"{Fore.BLUE}In this position: {Style.RESET_ALL}" + str(source_dic[KEYWORD_POSITION]) + f"{Fore.BLUE} there are these data in the parameter range: \n\n{Style.RESET_ALL}" + source_dic[VALUE] + "\n")

            elif source_dic[DIAGNOSIS] == OUT_OF_AVERAGE:
                print ("\n" +  f"{Fore.RED}The source: {Style.RESET_ALL}" + str(source_dic[ID]) + " " + str(source_dic[URL]) + f"{Fore.RED} is out of tolerance, the value: {Style.RESET_ALL}" + str(source_dic[VALUE]) + f"{Fore.RED} ​​are to far of the average, the average is: {Style.RESET_ALL}" + str(provisional_average) + f"{Fore.RED} (adjust allowed average parameter or delete this source). {Style.RESET_ALL}" + "\n")

            elif source_dic[DIAGNOSIS] == None:
                print("\n" +  f"{Fore.GREEN}The source: {Style.RESET_ALL}" + str(source_dic[ID]) + " " + str(source_dic[URL]) + f"{Fore.GREEN} is OK {Style.RESET_ALL} \n")
        
        print("\n" + str(datetime.now())) 
        print ("____________________________________________END OF THE TEST___________________________________________\n\n")
    

    return average






