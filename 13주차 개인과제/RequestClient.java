import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner;

public class RequestClient {

    private String host;
    private int port;

    public RequestClient(String host, int port) {
        this.host = host;
        this.port = port;
    }

    public void start() {

        try (
                Socket socket = new Socket(host, port);
                BufferedReader in = new BufferedReader(
                        new InputStreamReader(socket.getInputStream(), "UTF-8"));
                PrintWriter out = new PrintWriter(socket.getOutputStream(), true); 
                Scanner scanner = new Scanner(System.in)
        ) {
            System.out.println("[INFO] 서버에 연결되었습니다: " + host + ":" + port);

            while (true) {
                System.out.println();
                System.out.println("==== 메뉴 ====");
                System.out.println("1. 덧셈 (ADD a b)");
                System.out.println("2. 뺄셈 (SUB a b)");
                System.out.println("3. 곱셈 (MUL a b)");
                System.out.println("4. 나눗셈 (DIV a b)");
                System.out.println("5. 서버 시간 요청 (TIME)");
                System.out.println("6. 종료 (QUIT)");
                System.out.print("메뉴 선택: ");

                String choice = scanner.nextLine().trim();

                String request;

                switch (choice) {
                    case "1":
                        System.out.print("첫 번째 수 a 입력: ");
                        String a1 = scanner.nextLine().trim();
                        System.out.print("두 번째 수 b 입력: ");
                        String b1 = scanner.nextLine().trim();
                        request = "ADD " + a1 + " " + b1;
                        break;
                    case "2":
                        System.out.print("첫 번째 수 a 입력: ");
                        String a2 = scanner.nextLine().trim();
                        System.out.print("두 번째 수 b 입력: ");
                        String b2 = scanner.nextLine().trim();
                        request = "SUB " + a2 + " " + b2;
                        break;
                    case "3":
                        System.out.print("첫 번째 수 a 입력: ");
                        String a3 = scanner.nextLine().trim();
                        System.out.print("두 번째 수 b 입력: ");
                        String b3 = scanner.nextLine().trim();
                        request = "MUL " + a3 + " " + b3;
                        break;
                    case "4":
                        System.out.print("첫 번째 수 a 입력: ");
                        String a4 = scanner.nextLine().trim();
                        System.out.print("두 번째 수 b 입력: ");
                        String b4 = scanner.nextLine().trim();
                        request = "DIV " + a4 + " " + b4;
                        break;
                    case "5":
                        request = "TIME";
                        break;
                    case "6":
                        request = "QUIT";
                        break;
                    default:
                        System.out.println("[WARN] 잘못된 선택입니다.");
                        continue;
                }


                  out.println(request);


                String response = in.readLine();
                if (response == null) {
                    System.out.println("[INFO] 서버 연결이 끊어졌습니다.");
                    break;
                }

                System.out.println("[서버 응답] " + response);

                if ("QUIT".equalsIgnoreCase(request)) {
                    System.out.println("[INFO] 클라이언트를 종료합니다.");
                    break;
                }
            }

        } catch (IOException e) {
            System.out.println("[ERROR] 서버와 통신 중 오류: " + e.getMessage());
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("서버 IP 입력 (예: 192.168.0.10): ");
        String host = scanner.nextLine().trim();

        int port = 2500; // 서버와 동일하게
        RequestClient client = new RequestClient(host, port);
        client.start();
    }
}
