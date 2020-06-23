package os318Echo;
import java.io.*;
import java.net.*;
public class EchoServer {

	public static void main(String[] args) {
		try {
			ServerSocket Sock = new ServerSocket(6013);
			while (true) {
				Socket client = Sock.accept();
				InputStream inStream = client.getInputStream();
				OutputStream outStream = client.getOutputStream();
				int read;
				byte[] buffer = new byte[4 * 1024];
				read = inStream.read(buffer);
				while (read != -1) {
					outStream.write(buffer, 0, read);
				}
				inStream.close();
				outStream.close();
				client.close();
			}
		}catch(IOException ioe){
			System.err.println(ioe);
		}

	}

}
