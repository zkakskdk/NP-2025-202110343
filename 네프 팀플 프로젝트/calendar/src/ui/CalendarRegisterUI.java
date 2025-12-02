import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class CalendarRegisterUI extends JFrame {

    private JTextField txtCalendarName;
    private JTextArea txtDescription;
    private JComboBox<String> comboType;
    private JTextField txtOwner;
    private JButton btnSave;
    private JButton btnCancel;

    public CalendarRegisterUI() {
        setTitle("캘린더 등록");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(500, 400);
        setLocationRelativeTo(null);

        initComponents();
    }

    private void initComponents() {
        JPanel panel = new JPanel();
        panel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        panel.setLayout(new BorderLayout(10, 10));

        JLabel lblTitle = new JLabel("캘린더 등록", SwingConstants.CENTER);
        lblTitle.setFont(new Font("맑은 고딕", Font.BOLD, 20));
        panel.add(lblTitle, BorderLayout.NORTH);

        JPanel formPanel = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        gbc.gridx = 0; gbc.gridy = 0;
        formPanel.add(new JLabel("캘린더 이름"), gbc);

        txtCalendarName = new JTextField();
        gbc.gridx = 1; gbc.gridy = 0; gbc.weightx = 1.0;
        formPanel.add(txtCalendarName, gbc);

        gbc.gridx = 0; gbc.gridy = 1; gbc.weightx = 0;
        formPanel.add(new JLabel("캘린더 유형"), gbc);

        comboType = new JComboBox<>(new String[]{"개인 캘린더", "팀 캘린더"});
        gbc.gridx = 1; gbc.gridy = 1; gbc.weightx = 1.0;
        formPanel.add(comboType, gbc);

        gbc.gridx = 0; gbc.gridy = 2;
        formPanel.add(new JLabel("소유자 / 팀 이름"), gbc);

        txtOwner = new JTextField();
        gbc.gridx = 1; gbc.gridy = 2;
        formPanel.add(txtOwner, gbc);

        gbc.gridx = 0; gbc.gridy = 3;
        formPanel.add(new JLabel("설명"), gbc);

        txtDescription = new JTextArea(5, 20);
        txtDescription.setLineWrap(true);
        txtDescription.setWrapStyleWord(true);
        JScrollPane scrollDesc = new JScrollPane(txtDescription);

        gbc.gridx = 1; gbc.gridy = 3; gbc.weightx = 1.0; gbc.weighty = 1.0;
        gbc.fill = GridBagConstraints.BOTH;
        formPanel.add(scrollDesc, gbc);

        panel.add(formPanel, BorderLayout.CENTER);

        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        btnSave = new JButton("저장");
        btnCancel = new JButton("취소");
        buttonPanel.add(btnCancel);
        buttonPanel.add(btnSave);

        panel.add(buttonPanel, BorderLayout.SOUTH);

        btnSave.addActionListener(e -> onSave());
        btnCancel.addActionListener(e -> dispose());

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
                    "입력 오류", JOptionPane.WARNING_MESSAGE);
            return;
        }

        String message = String.format(
                "캘린더 등록 완료!\n\n이름: %s\n유형: %s\n소유자/팀: %s\n설명: %s",
                name, type, owner, desc);

        JOptionPane.showMessageDialog(this, message);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            CalendarRegisterUI frame = new CalendarRegisterUI();
            frame.setVisible(true);
        });
    }
}

