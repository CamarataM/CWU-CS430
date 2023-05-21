// Needed to continue using 'sprintf', although these should be replaced by 'sprintf_s' instead of silencing the warning.
#define _CRT_SECURE_NO_WARNINGS

#include<stdio.h>
#include <stdbool.h>
#include "stego.h"

int main(int argc, const char* argv[])
{
	if (argc != 3)
	{
		fprintf(stderr, "\nUsage: %s stegoImage outData\n\n", argv[0]);
		fprintf(stderr, "where stegoImage == filename for image containing stego data\n");
		fprintf(stderr, "      outData == data read from stegoImage file\n\n");
		exit(0);
	}

	FILE* in;
	FILE* outdata;

	char infname[80];
	size_t argv1Length = strlen(argv[1]);
	sprintf(infname, argv[1]);
	in = fopen(infname, "r");
	if (in == NULL)
	{
		fprintf(stderr, "\nError opening file %s\n\n", infname);
		exit(0);
	}

	char outdatafname[80];
	size_t argv2Length = strlen(argv[2]);
	sprintf(outdatafname, argv[2]);
	outdata = fopen(outdatafname, "w");
	if (outdata == NULL)
	{
		fprintf(stderr, "\nError opening file %s\n\n", outdatafname);
		exit(0);
	}

	char temp;
	char data = 0;

	int dataBytes = 0;
	while (1)
	{
		int x = fscanf(in, "%c", &temp);
		if (x != 1)
		{
			break;
		}
		++dataBytes;
	}

	fseek(in, 0, SEEK_SET);

	//fclose(in);
	//in = fopen(infname, "r");

	int shft = 0;

	bool inStegoHeader = false;
	int stegoHeaderIndex = 0;
	int j = 0;
	int ttt = 0;
	int stegoHeaderByteReplacement = 0;

	bool inInsertedBits = false;
	int insertedBitsIndex = 0;
	int insertedBitsByteReplacement = 1;

	int dataBitsByteReplacement = 2;

	for (int i = 0; i < dataBytes; ++i)
	{
		int x = fscanf(in, "%c", &temp);
		if (x != 1)
		{
			fprintf(stderr, "\nError in file %s\n\n", infname);
			exit(0);
		}

		if (i >= START_FROM && !inStegoHeader && stegoHeaderIndex == 0) {
			inStegoHeader = true;
		}

		if (!inStegoHeader && stegoHeaderIndex != 0 && !inInsertedBits && insertedBitsIndex == 0) {
			inInsertedBits = true;
		}

		if (inInsertedBits) {
			insertedBitsIndex++;

			// Zero out inserted bits.
			temp = insertedBitsByteReplacement;

			if (insertedBitsIndex >= 27) {
				inInsertedBits = false;
			}
		}

		if (inStegoHeader) {
			ttt ^= ((temp & 0x1) << j);

			j++;
			stegoHeaderIndex++;
			if (j >= 8) {
				j = 0;

				if (ttt != 0xa5)
				{
					fprintf(stderr, "\nError --- file does not contain stego data that I can read. ttt=%i\n\n", ttt);
					exit(0);
				}
				else {
					fprintf(stderr, "\nValid ttt value\n\n");
				}

				ttt = 0;
			}

			if (stegoHeaderIndex >= 64) {
				inStegoHeader = false;
			}

			// Zero out Stego header.
			temp = stegoHeaderByteReplacement;
		}

		if (!inInsertedBits && insertedBitsIndex != 0 && !inStegoHeader && stegoHeaderIndex != 0) {
			fprintf(stderr, "\n1: %i\n", temp);
			temp = temp & 0x11111111;
			fprintf(stderr, "\n2: %i\n", temp);

			//data = data ^ ((temp & 0x1) << shft);
			//++shft;
			//if (shft == 8)
			//{
			//	//fprintf(stderr, "\n1: %i\n", temp);
			//	//fprintf(stderr, "\n2: %i\n", data);

			//	//temp = dataBitsByteReplacement;
			//	//temp = temp ^ 0x0;

			//	if (data > 0) {
			//		temp = temp - data;
			//	}

			//	data = 0;
			//	shft = 0;
			//}
		}

		fprintf(outdata, "%c", temp);
	}

	printf("\n");

	fclose(in);
	fclose(outdata);
}