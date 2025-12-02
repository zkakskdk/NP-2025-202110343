import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class CalendarRegisterUI extends JFrame {

    private JTextField txtCalendarName;     // 캘린더 이름
    private JTextArea txtDescription;       // 설명
    private JComboBox<String> comboType;    // 개인 / 팀 캘린더
    private JTextField txtOwner;            // 소유자/팀 이름
    private JButton btnSave;
    private JButton btnCancel;

    public CalendarRegisterUI() {
        setTitle("캘린더 등록");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(500, 400);
        setLocationRelativeTo(null); // 화면 가운데

        initComponents();
    }

    private void initComponents() {
        // 메인 패널
        JPanel panel = new JPanel();
        panel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        panel.setLayout(new BorderLayout(10, 10));

        // --------- 상단 제목 ---------
        JLabel lblTitle = new JLabel("캘린더 등록", SwingConstants.CENTER);
        lblTitle.setFont(new Font("맑은 고딕", Font.BOLD, 20));
        panel.add(lblTitle, BorderLayout.NORTH);

        // --------- 중앙 입력 영역 ---------
        JPanel formPanel = new JPanel();
        formPanel.setLayout(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        // 1. 캘린더 이름
        gbc.gridx = 0;
        gbc.gridy = 0;
        formPanel.add(new JLabel("캘린더 이름"), gbc);

        txtCalendarName = new JTextField();
        gbc.gridx = 1;
        gbc.gridy = 0;
        gbc.weightx = 1.0;
        formPanel.add(txtCalendarName, gbc);

        // 2. 캘린더 유형 (개인 / 팀)
        gbc.gridx = 0;
        gbc.gridy = 1;
        gbc.weightx = 0;
        formPanel.add(new JLabel("캘린더 유형"), gbc);

        comboType = new JComboBox<>(new String[]{"개인 캘린더", "팀 캘린더"});
        gbc.gridx = 1;
        gbc.gridy = 1;
        gbc.weightx = 1.0;
        formPanel.add(comboType, gbc);

        // 3. 소유자 / 팀 이름
        gbc.gridx = 0;
        gbc.gridy = 2;
        gbc.weightx = 0;
        formPanel.add(new JLabel("소유자 / 팀 이름"), gbc);

        txtOwner = new JTextField();
        gbc.gridx = 1;
        gbc.gridy = 2;
        gbc.weightx = 1.0;
        formPanel.add(txtOwner, gbc);

        // 4. 설명(멀티라인)
        gbc.gridx = 0;
        gbc.gridy = 3;
        gbc.weightx = 0;
        gbc.anchor = GridBagConstraints.NORTH;
        formPanel.add(new JLabel("설명"), gbc);

        txtDescription = new JTextArea(5, 20);
        txtDescription.setLineWrap(true);
        txtDescription.setWrapStyleWord(true);
        JScrollPane scrollDesc = new JScrollPane(txtDescription);

        gbc.gridx = 1;
        gbc.gridy = 3;
        gbc.weightx = 1.0;
        gbc.weighty = 1.0;
        gbc.fill = GridBagConstraints.BOTH;
        formPanel.add(scrollDesc, gbc);

        panel.add(formPanel, BorderLayout.CENTER);

        // --------- 하단 버튼 영역 ---------
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));

        btnSave = new JButton("저장");
        btnCancel = new JButton("취소");

        buttonPanel.add(btnCancel);
        buttonPanel.add(btnSave);

        panel.add(buttonPanel, BorderLayout.SOUTH);

        // 버튼 이벤트
        btnSave.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                onSave();
            }
        });

        btnCancel.addActionListener(e -> onCancel());

        setContentPane(panel);
    }

    private void onSave() {
        String name = txtCalendarName.getText().trim();
        String type = (String) comboType.getSelectedItem();
        String owner = txtOwner.getText().trim();
        String desc = txtDescription.getText().trim();

        if (name.isEmpty()) {
            JOptionPane.showMessageDialog(this,
                    "캘린더 이름을 입력하세요.",
                    "입력 오류",
                    JOptionPane.WARNING_MESSAGE);
            return;
        }

        // 실제로는 여기서 DB 저장이나 서버 전송 등을 수행
        String message = String.format(
                "캘린더 등록 정보\n\n" +
                "이름: %s\n유형: %s\n소유자/팀: %s\n설명: %s",
                name, type, owner, desc);

        JOptionPane.showMessageDialog(this,
                message,
                "등록 완료(샘플)",
                JOptionPane.INFORMATION_MESSAGE);
    }

    private void onCancel() {
        // 입력 값 초기화 또는 창 닫기
        int result = JOptionPane.showConfirmDialog(
                this,
                "입력을 취소하고 창을 닫을까요?",
                "취소 확인",
                JOptionPane.YES_NO_OPTION
        );
        if (result == JOptionPane.YES_OPTION) {
            dispose(); // 창 닫기
        }
    }

    public static void main(String[] args) {
        // 항상 EDT에서 실행
        SwingUtilities.invokeLater(() -> {
            CalendarRegisterUI frame = new CalendarRegisterUI();
            frame.setVisible(true);
        });
    }
}
