package os318Echo;
import java.io.*;
import java.net.*;
public class EchoClient {

	public static void main(String[] args) {
		try {
			Socket Sock = new Socket("127.0.0.1", 6013);
			PrintWriter outStream = new PrintWriter(Sock.getOutputStream());
			outStream.println("data");				
			outStream.flush();	
			BufferedReader buffer = new BufferedReader(new InputStreamReader(Sock.getInputStream()));
			String Text = buffer.readLine();
			System.out.println(Text);
			Sock.close();
		}catch(IOException ioe){
			System.err.println(ioe);
		}
	}
}
