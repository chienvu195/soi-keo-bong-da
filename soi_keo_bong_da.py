import streamlit as st

st.set_page_config(page_title="App Soi Kèo Bóng Đá", layout="centered")

st.title("⚽ APP SOI KÈO BÓNG ĐÁ")
st.write("Soi **Tài/Xỉu + % xác suất** (tham khảo)")

# ===== INPUT =====
st.header("📥 Nhập dữ liệu trận đấu")

avg_goal = st.number_input("Tổng bàn TB 2 đội (gần đây)", 0.0, 6.0, 2.6, 0.1)
keo_tx = st.selectbox("Kèo T/X", [2.0, 2.25, 2.5, 2.75, 3.0])

defense = st.selectbox("Chất lượng hàng thủ", ["chặt", "trung bình", "kém"])

tai_rate = st.slider("% trận ra TÀI gần đây", 0, 100, 60)
xiu_rate = 100 - tai_rate

form = st.slider("Phong độ đội mạnh hơn (0–100)", 0, 100, 65)
goal = st.slider("Khả năng ghi bàn (0–100)", 0, 100, 70)
home = st.selectbox("Sân nhà?", ["Có", "Không"])
h2h = st.slider("Đối đầu (0–100)", 0, 100, 60)
market = st.slider("Biến động kèo có lợi? (0–100)", 0, 100, 55)

# ===== LOGIC TÀI XỈU =====
def soi_tai_xiu():
    tai = 0
    xiu = 0

    if avg_goal >= keo_tx + 0.3:
        tai += 2
    elif avg_goal <= keo_tx - 0.3:
        xiu += 2

    if defense == "kém":
        tai += 1
    elif defense == "chặt":
        xiu += 1

    tai += tai_rate / 100
    xiu += xiu_rate / 100

    if tai - xiu >= 2:
        return "🔥 NÊN ĐÁNH TÀI", tai, xiu
    elif xiu - tai >= 2:
        return "🧊 NÊN ĐÁNH XỈU", tai, xiu
    else:
        return "⚖️ KÈO CÂN – NÉ", tai, xiu

# ===== LOGIC % =====
def tinh_xac_suat():
    score = 0
    score += (form / 100) * 0.3
    score += (goal / 100) * 0.25
    score += (1 if home == "Có" else 0) * 0.15
    score += (h2h / 100) * 0.15
    score += (market / 100) * 0.15

    percent = round(score * 100, 1)

    if percent >= 65:
        note = "✅ KÈO ĐẸP – CÓ THỂ ĐÁNH"
    elif percent >= 55:
        note = "⚠️ KÈO TRUNG BÌNH – ĐÁNH NHỎ"
    else:
        note = "❌ KÈO XẤU – NÉ"

    return percent, note

# ===== OUTPUT =====
if st.button("🔍 SOI KÈO"):
    kq_tx, tai, xiu = soi_tai_xiu()
    percent, note = tinh_xac_suat()

    st.header("📊 KẾT QUẢ")
    st.subheader(kq_tx)
    st.write(f"Điểm Tài: {round(tai,2)} | Điểm Xỉu: {round(xiu,2)}")

    st.subheader(f"🎯 Xác suất: {percent}%")
    st.write(note)

    st.info("⚠️ Chỉ nên đánh khi **Tài/Xỉu + % xác suất cùng hướng**")
