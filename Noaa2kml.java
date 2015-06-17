/** 
 *  @author Jordan Christiansen
 *  @since 2015-06-10
 *
 *  Read a list of geospactial coordinates from a CSV file from NOAA and
 *  translate it into a KML file.
 */

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.Scanner;

public class Noaa2kml
{
	private static String progName = "Noaa2kml";

	public static void main(String[] args)
	{
		// Make sure we have the right number of arguments.
		if (args.length != 3) printUsage();
		Path locationsPath = Paths.get(args[0]);
		Path detailsPath = Paths.get(args[1]);
		Path outputPath = Paths.get(args[2]);

		// Check if the files exist.
		if (!Files.exists(locationsPath))
		{
			System.err.format("No such file \"%s\"\n", locationsPath);
			System.exit(1);
		}
		if (!Files.exists(detailsPath))
		{
			System.err.format("No such file \"%s\"\n", detailsPath);
			System.exit(1);
		}
		if (Files.exists(outputPath))
		{
			Scanner userInput = new Scanner(System.in);
			System.out.format("%s already exists. Overwrite it? [y/N] ", args[2]);
			String userResponse = userInput.nextLine();
			if (userResponse == null || !userResponse.startsWith("y"))
			{
				System.exit(0);
			}
		}

		// These strings contain the text of the resulting KML document.
		String header  = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" +
						 "<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n" +
						 "<Folder>\n";
		String body    = "";
		String section = "\t<Placemark>\n" +
						 "\t\t<name>%s</name>\n" +
						 "\t\t<Point>\n" +
						 "\t\t\t<coordinates>%s,%s</coordinates>\n" +
						 "\t\t</Point>\n" +
						 "\t</Placemark>\n";
		String footer  = "</Folder>\n" +
						 "</kml>\n";

		// Parse the input files and build the string containing the body of
		// the KML document as we go.
		try (BufferedReader locations =
				Files.newBufferedReader(locationsPath))
		{
			String line;
			while ((line = locations.readLine()) != null)
			{
				String[] lineFields = line.split(",");

				// Skip the line if its eventID isn't a number (this skips the
				// header line)
				try {
					Integer.parseInt(lineFields[2]);
				} catch (NumberFormatException e) {
					continue;
				}

				String name = findEventType(detailsPath, lineFields[2]);
				String latitude = lineFields[7];
				String longitude = lineFields[8];

				body += String.format(section, name, longitude, latitude);
			}
		}
		catch (IOException e)
		{
			System.err.format("IOException: %s%n", e);
		}

		// Write the resulting KML to a file.
		try (BufferedWriter outputFile =
				Files.newBufferedWriter(outputPath, StandardCharsets.UTF_8))
		{
			outputFile.write(header + body + footer);
		}
		catch (IOException e)
		{
			System.err.format("IOException: %s%n", e);
		}
	}

	/**
	 * Look up the event type in the details file.
	 */
	private static String findEventType(Path filePath, String eventID)
	{
		try (BufferedReader details = Files.newBufferedReader(filePath))
		{
			String line;
			while ((line = details.readLine()) != null)
			{
				if (line.contains(eventID))
				{
					String eventType = line.split(",")[12];
					return eventType.substring(1, eventType.length()-1);
				}
			}
		}
		catch (IOException exception)
		{
			System.err.format("IOException: %s%n", exception);
		}

		return null;
	}

	/**
	 * Print the usage message and exit the program.
	 */
	private static void printUsage()
	{
		System.out.format(
				"Usage: %s LOCATIONS_FILE DETAILS_FILE OUTPUT\n", progName);
		System.exit(0);
	}
}
