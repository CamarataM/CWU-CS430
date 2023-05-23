// Needed to continue using 'sprintf', although this should be replaced by 'sprintf_s' instead of silencing the warning.
#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdbool.h>
#include "stego.h"

// Will remove any stego data from a character, even if that data is not actually stego data.
char removeStego(char character, bool roundToNearest) {
	if (roundToNearest) {
		int characterInt = (int)character;

		// Check if character is a positive number. If not, compute its positive value by taking the negative number and adding it to 265 (max + 1 of character).
		if (character < 0) {
			characterInt = 256 + character;
		}

		if (characterInt >= 254) {
			return 255;
		}
		else {
			return 0;
		}
	}

	// If we don't need to attempt a repair, return the character with the least significant (furthest-right) bit masked out. This means that 255 will be equal to 254, while 0 stays the same.
	//return character & 0b11111110;

	// This will instead always set the final bit to 1 regardless of the value of the original image. Means that values greater than 254 will be equal to 255, while 0 will be equal to 1.
	return character | 0b00000001;
}

int main(int argc, const char* argv[])
{
	// Controls whether detected stego headers, inserted bits, and stego data should be kept in the output file.
	bool keepStegoHeader = false;
	bool keepInsertedBits = false;
	bool keepStegoData = false;

	// Controls whether the program should exit if an invalid stego header is detected. Turning this to false will likely produce a malformed file.
	bool exitOnInvalidStegoHeader = true;

	// Whether rounding should be used for removing stego data. This is capable of producing the original image from an image with stego data only if the image is monochromatic, as it will round up values from 254 to 255 (inclusive) or round down values from 1 to 0 (inclusive).
	bool roundToNearest = true;

	if (argc != 3)
	{
		fprintf(stderr, "\nUsage: %s stegoImage outData\n\n", argv[0]);
		fprintf(stderr, "where stegoImage == filename for image containing stego data\n");
		fprintf(stderr, "      outData == data read from stegoImage file\n\n");
		exit(0);
	}

	// Read both the inpput and output file names from the arguments passed to the program and attempt to open them, exiting the program if an error is encountered.
	FILE* inputFile;
	FILE* outputFile;

	// This should really be taken from the system enviroment variables, as paths can be a lot longer than 255 in modern day.
	char inputFileNmae[255];
	sprintf(inputFileNmae, argv[1]);
	inputFile = fopen(inputFileNmae, "r");
	if (inputFile == NULL)
	{
		fprintf(stderr, "\nError opening file %s\n\n", inputFileNmae);
		exit(0);
	}

	char outputFileName[255];
	sprintf(outputFileName, argv[2]);
	outputFile = fopen(outputFileName, "w");
	if (outputFile == NULL)
	{
		fprintf(stderr, "\nError opening file %s\n\n", outputFileName);
		exit(0);
	}

	// Initialize the variables required for the main logic loop.
	char fileChar;

	int shift = 0;

	bool inStegoHeader = false;
	int stegoHeaderIndex = 0;
	int j = 0;
	int ttt = 0;
	int stegoHeaderByteReplacement = 0;

	bool inInsertedBits = false;
	int insertedBitsIndex = 0;
	int insertedBitsByteReplacement = 1;

	int dataBitsByteReplacement = 2;

	int fileCharIndex = 0;
	// While an error is not returned from scanning the next char into 'fileChar'...
	while (fscanf(inputFile, "%c", &fileChar) == 1)
	{
		// If the current file char index is greater than or equal to the start from and we are not in the stego header and we haven't read the stego header, then we are in the stego header.
		if (fileCharIndex >= START_FROM && !inStegoHeader && stegoHeaderIndex == 0) {
			inStegoHeader = true;
		}

		// If we are not in the stego header and we have read the stego header and we are not in the inserted bits index and we haven't read the inserted bits, then we are in the inserted bits section.
		if (!inStegoHeader && stegoHeaderIndex != 0 && !inInsertedBits && insertedBitsIndex == 0) {
			inInsertedBits = true;
		}

		// If we are in the inserted bits section, read 27 bits and remove if we are set to not keep the inserted bits.
		if (inInsertedBits) {
			insertedBitsIndex++;

			if (!keepInsertedBits) {
				fileChar = removeStego(fileChar, roundToNearest);
			}

			if (insertedBitsIndex >= 27) {
				inInsertedBits = false;
			}
		}

		// If we are in the stego header, check that the header data is valid using the same formula as stegoRead. If we are not supposed to keep the stego header, replace the bits with 0x0.
		if (inStegoHeader) {
			ttt ^= ((fileChar & 0x1) << j);

			j++;
			stegoHeaderIndex++;
			if (j >= 8) {
				j = 0;

				if (ttt != 0xa5)
				{
					fprintf(stderr, "\nError --- file does not contain stego data that I can read. ttt=%i\n\n", ttt);

					if (exitOnInvalidStegoHeader) {
						exit(0);
					}
				}

				ttt = 0;
			}

			if (stegoHeaderIndex >= 64) {
				inStegoHeader = false;
			}

			if (!keepStegoHeader) {
				fileChar = removeStego(fileChar, roundToNearest);
			}
		}

		// If we have processed the inserted bits and stego header sections, we are in the actual data of the file. Remove the stego from the char.
		if (!keepStegoData && !inInsertedBits && insertedBitsIndex != 0 && !inStegoHeader && stegoHeaderIndex != 0) {
			fileChar = removeStego(fileChar, roundToNearest);
		}

		// Print the (either modified or unmodified) char value into the output file.
		fprintf(outputFile, "%c", fileChar);

		fileCharIndex++;
	}

	printf("\n");

	// Close both of the files.
	fclose(inputFile);
	fclose(outputFile);
}