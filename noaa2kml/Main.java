/** 
 *  @author Jordan Christiansen
 *  @since 2015-06-10
 *
 *  Read a list of geolocation coordinates from a CSV file from NOAA and
 *  translate it into a KML file.
 */
package noaa2kml;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.ArrayList;

public class Main
{
	private static String progName = "Noaa2kml";
	private static final int maxThreads = 4;

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
			Console userInput = System.console();
			System.out.format("%s already exists. Overwrite it? [y/N] ", args[2]);
			String userResponse = userInput.readLine();
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

		/*
		 * This is where I will start spawning the reader threads. The strategy
		 * will be to have each thread process a set number of entries (say
		 * 100) and when the thread finishes, main will start a new one to keep
		 * the number of threads below a minimum.
		 */
		try (BufferedReader inputFile = Files.newBufferedReader(locationsPath))
		{
			ArrayList<Thread> threads = new ArrayList<Thread>(maxThreads);
			String line = "";
			String dataChunk = "";

			while (line != null)
			{
				for (int i = 0; i < 100; i++)
				{
					line = inputFile.readLine();
					dataChunk += line;
				}

				if (threads.size() >= maxThreads)
				{
					Thread.currentThread().wait();
				}

				for (Thread thread : threads)
				{
					if (!thread.isAlive())
					{
						//body += String.format(section, thread.getEventType()); What am I doing?? Pull it together, man.
						threads.remove(thread);
					}
				}

				dataChunk = "";
			}
		}
		catch (IOException exception)
		{
			System.err.format("IOException: %s%n", exception);
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
	 * Print the usage message and exit the program.
	 */
	private static void printUsage()
	{
		System.out.format(
				"Usage: %s LOCATIONS_FILE DETAILS_FILE OUTPUT\n", progName);
		System.exit(0);
	}
}
