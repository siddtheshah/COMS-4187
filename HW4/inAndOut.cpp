// Siddhant Shah
// g++ inAndOut.cpp -o inAndOut.o -ggdb -g && ./inAndOut.o 


#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <iostream>
#include <fstream>

using namespace std;

int main()
{
	ifstream inFile;
	ofstream outFile;
	string line;

	inFile.open("in.txt", ios::in);
	outFile.open("out.txt", ios::out);

	while ( getline(inFile, line))
	{
		outFile << line << '\n';
	}



}