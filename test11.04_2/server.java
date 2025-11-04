import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;

public class server {
    private final int port;

    public server(int port) {
        this.port = port;
    }

    public void start() throws IOException {
        try (ServerSocket server = new ServerSocket(port)) {
            System.out.println("[N-ECHO(Simple-Java)] listening on 0.0.0.0:" + port);
            while (true) {
                Socket client = server.accept();
                System.out.println("[N-ECHO(Simple-Java)] client " + client.getRemoteSocketAddress() + " connected");
                new Thread(() -> handle(client)).start();
            }
        }
    }

    private void handle(Socket socket) {
        try (socket) {
            socket.setSoTimeout(300); // 길이/개행이 없으므로 짧은 타임아웃으로 '한 번에 보낸 데이터' 수집
            InputStream in = new BufferedInputStream(socket.getInputStream());
            ByteArrayOutputStream buf = new ByteArrayOutputStream();

            byte[] tmp = new byte[4096];
            while (true) {
                try {
                    int r = in.read(tmp);
                    if (r == -1) break;        // 연결 종료
                    buf.write(tmp, 0, r);
                    if (in.available() == 0) { // 더 들어온 게 없으면 종료
                        break;
                    }
                } catch (SocketTimeoutException e) {
                    break; // 잠시 기다렸는데 더 안 오면 '요청 완성'으로 간주
                }
            }

            String text = buf.toString(StandardCharsets.UTF_8).trim();
            // 기대 형식: "n msg"
            int sp = text.indexOf(' ');
            if (sp < 0) {
                writeUtf8(socket, "[서버 오류] 형식은 'n msg' 입니다.");
                return;
            }

            String nStr = text.substring(0, sp).trim();
            String msg  = text.substring(sp + 1);
            int n;
            try {
                n = Integer.parseInt(nStr);
            } catch (NumberFormatException e) {
                writeUtf8(socket, "[서버 오류] n은 정수여야 합니다.");
                return;
            }
            if (n < 1) {
                writeUtf8(socket, "[서버 오류] n은 1 이상이어야 합니다.");
                return;
            }

            // 클라가 recv(1024) '한 번'만 하므로, N줄을 한꺼번에 보낸다.
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) {
                if (i > 0) sb.append('\n');
                sb.append(msg);
            }
            writeUtf8(socket, sb.toString());

        } catch (IOException e) {
            System.err.println("[ERROR] " + e.getMessage());
        }
    }

    private void writeUtf8(Socket socket, String s) throws IOException {
        OutputStream out = socket.getOutputStream();
        out.write(s.getBytes(StandardCharsets.UTF_8));
        out.flush();
    }

    public static void main(String[] args) throws IOException {
        int port = (args.length > 0) ? Integer.parseInt(args[0]) : 2500; // 네 클라 기본 포트 2500
        new server(port).start();
    }
}
