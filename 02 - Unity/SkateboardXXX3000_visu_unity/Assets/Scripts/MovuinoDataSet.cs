using System;
using System.IO;
using System.Globalization;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Movuino
{
    public class MovuinoDataSet
    {

        private string dataPath;
        List<object[]> rawData = new List<object[]>();

        object[] time;
        object[] acceleration;
        object[] gyroscope;
        object[] magnetometer;

        object[] theta;
        object[] velocity;
        object[] pos;

        float[] normAccel;
        float[] normGyr;


        public MovuinoDataSet(string dataPath)
        {
            Debug.Log("Reading... " + dataPath);
            rawData = ReadCSV(dataPath);

            
        }

        List<object[]> ReadCSV(string dataPath)
        {

            StreamReader sr = new StreamReader(dataPath);
            char sep = ',';

            string line = sr.ReadLine();

            //We'ra counting the number of column
            int nb_columne = 1;
            foreach (char a in line)
            {
                if (a == sep)
                    nb_columne++;
            }
            List<object[]> data = new List<object[]>(); //All the file
            object[] tData = new object[nb_columne]; //Data for a t time that has a 
            string value = "";
            int i = 0;

            //Header
            foreach (char a in line)
            {
                if (a == ',')
                {
                    tData[i] = value;
                    
                    value = "";
                    i += 1;
                }
                else
                {
                    value += a;
                }

            }
            tData[i] = value;
            data.Add(tData);
            tData = new object[nb_columne];
            value = "";
            line = sr.ReadLine();

            //Data
            while (line != null)
            {
                i = 0;
                //We read all the line
                foreach (char a in line)
                {
                    if (a == ',')
                    {
                        tData[i] = float.Parse(value, CultureInfo.InvariantCulture);
                        value = "";
                        i += 1;
                    }
                    else
                    {
                        value += a;
                    }

                }
                tData[i] = float.Parse(value, CultureInfo.InvariantCulture);
                data.Add(tData);
                tData = new object[nb_columne];
                value = "";
                line = sr.ReadLine();
            }
            Debug.Log(data[0][1]);
            return data;
        }



    }


}