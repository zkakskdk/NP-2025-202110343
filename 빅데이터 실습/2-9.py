def set_menu():
    main = ['라면', '공깃밥', '돈까스', '냉면']
    topping = ['계란', '치즈']
    menu = []

    # --- 빈칸 부분 시작 ---
    for m in main:
        for t in topping:
            # '냉면'에 '치즈' 토핑인 경우만 제외
            if m == '냉면' and t == '치즈':
                continue
            # 유효한 조합을 튜플 형태로 리스트에 추가
            menu.append((m, t))
    # --- 빈칸 부분 끝 ---

    return menu

print(set_menu())