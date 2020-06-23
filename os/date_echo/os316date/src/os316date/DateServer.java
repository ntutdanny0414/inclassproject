package os316date;
import java.net.*;
import java.io.*;
public class DateServer {
    public static void main(String[] args) {
        try {
        	ServerSocket sock = new ServerSocket(6017);
        	while (true) {
            Socket client = sock.accept();
            PrintWriter pout = new PrintWriter(client.getOutputStream(), true);
            String quote = "quote";
            pout.println(quote.toString());
            client.close();
        	}
        } catch (IOException ioe) {
            System.err.println(ioe);
        }
    }
}