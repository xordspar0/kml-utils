package noaa2kml;

import java.io.*;
import java.nio.file.*;

public class EventFinder extends Thread
{
	private String data;
	private Path filePath;
	private String eventID;
	private String eventType;

	EventFinder(String data, Path filePath, String eventID)
	{
		this.data = data;
		this.filePath = filePath;
		this.eventID = eventID;
	}

	/**
	 * Look up the event type in the details file.
	 */
	public void run()
	{
		try (BufferedReader details = Files.newBufferedReader(filePath))
		{
			String line;
			while ((line = details.readLine()) != null)
			{
				if (line.contains(eventID))
				{
					String eventType = line.split(",")[12];
					eventType = eventType.substring(1, eventType.length()-1);
				}
			}
		}
		catch (IOException exception)
		{
			System.err.format("IOException: %s%n", exception);
		}
	}

	String getEventType()
	{
		return eventType;
	}
}

