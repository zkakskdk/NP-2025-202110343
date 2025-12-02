import java.io.*;
import java.net.Socket;
import java.util.Scanner;

public class chatclient {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        try {
            System.out.print("서버 IP를 입력하세요: ");
            String serverIp = scanner.nextLine().trim();

            int serverPort = 2500; 

            System.out.print("사용할 닉네임을 입력하세요: ");
            String nickname = scanner.nextLine().trim();
            if (nickname.isEmpty()) {
                nickname = "익명";
            }

            Socket socket = new Socket(serverIp, serverPort);
            System.out.println("[시스템] 서버에 접속했습니다. (종료하려면 /exit 입력)");

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(socket.getInputStream(), "UTF-8"));
            BufferedWriter out = new BufferedWriter(
                    new OutputStreamWriter(socket.getOutputStream(), "UTF-8"));

            Thread receiveThread = new Thread(() -> {
                try {
                    String line;
                    while ((line = in.readLine()) != null) {
                        System.out.println();
                        System.out.println(line);
                        System.out.print("> ");
                    }
                } catch (IOException e) {
                    System.out.println("\n[시스템] 서버와의 연결이 종료되었습니다.");
                }
            });
            receiveThread.setDaemon(true);
            receiveThread.start();

            while (true) {
                System.out.print("> ");
                String msg = scanner.nextLine();
                if (msg.equals("/exit")) {
                    break;
                }

                String fullMsg = "[" + nickname + "] " + msg + "\n";
                out.write(fullMsg);
                out.flush();
            }

            System.out.println("[시스템] 연결을 종료합니다.");
            socket.close();
            scanner.close();

        } catch (Exception e) {
            System.out.println("[에러] " + e.getMessage());
            e.printStackTrace();
        }
    }
}
