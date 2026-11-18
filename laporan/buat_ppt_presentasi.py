"""
PPT presentasi — Simple IoT Hardware (DHT + LED + MQTT + Laravel).
Style mirip flow Uji End-to-End Tes_BNSP, disesuaikan project ini.
Screenshot: taruh file di folder bukti/ lalu jalankan ulang script
(atau sisipkan manual di PowerPoint — slot SS sudah berlabel).
"""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(r"D:\Tugas_Akhir\Simple_IoT_Laravel")
BUKTI = ROOT / "bukti"
OUT = ROOT / "laporan" / "Presentasi_Simple_IoT_MQTT_Laravel.pptx"

BLUE = RGBColor(0x5B, 0x9F, 0xD4)
GREEN = RGBColor(0x3E, 0xCF, 0x8E)
PINK = RGBColor(0xEF, 0x5F, 0x5F)
INK = RGBColor(0x1B, 0x1E, 0x28)
MUTED = RGBColor(0x8F, 0xA0, 0xB3)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BG = RGBColor(0xF5, 0xF6, 0xFA)
LINE = RGBColor(0xE8, 0xEA, 0xF0)
YELLOW = RGBColor(0xF0, 0xB4, 0x29)
DARK = RGBColor(0x18, 0x22, 0x30)


def run(p, text, size=16, bold=False, color=INK):
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    r.font.name = "Calibri"
    return r


def add_bg(slide):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    sh.line.fill.background()
    sh.fill.solid()
    sh.fill.fore_color.rgb = BG
    spTree = slide.shapes._spTree
    sp = sh._element
    spTree.remove(sp)
    spTree.insert(2, sp)


def card(slide, left, top, width, height, fill=WHITE):
    sh = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.color.rgb = LINE
    sh.adjustments[0] = 0.08
    return sh


def header(slide, title, subtitle):
    bar = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.35), Inches(0.25), Inches(12.6), Inches(0.95)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = DARK
    bar.line.fill.background()
    tf = bar.text_frame
    tf.clear()
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run(p, title, 24, True, WHITE)
    p2 = tf.add_paragraph()
    run(p2, subtitle, 13, False, GREEN)


def footer(slide, page=""):
    box = slide.shapes.add_textbox(Inches(0.4), Inches(7.15), Inches(12.5), Inches(0.28))
    p = box.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    txt = "Simple IoT · ESP32 DHT + LED · MQTT Mosquitto · Laravel 11 + MySQL"
    if page:
        txt = f"{txt}  ·  {page}"
    run(p, txt, 11, False, MUTED)


def meaning_box(slide, left, top, width, height, title, lines, accent=BLUE):
    card(slide, left, top, width, height)
    strip = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(0.12), Inches(height)
    )
    strip.fill.solid()
    strip.fill.fore_color.rgb = accent
    strip.line.fill.background()

    title_box = slide.shapes.add_textbox(
        Inches(left + 0.25), Inches(top + 0.12), Inches(width - 0.35), Inches(0.35)
    )
    run(title_box.text_frame.paragraphs[0], title, 14, True, accent)

    body = slide.shapes.add_textbox(
        Inches(left + 0.25), Inches(top + 0.48), Inches(width - 0.4), Inches(height - 0.6)
    )
    tf = body.text_frame
    tf.word_wrap = True
    first = True
    for line in lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        run(p, line, 13, False, INK)
        p.space_after = Pt(3)


def ss_slot(slide, left, top, width, height, label, filename):
    """Placeholder screenshot — teman isi file di bukti/ lalu regenerate / tempel manual."""
    sh = card(slide, left, top, width, height, RGBColor(0xEE, 0xF2, 0xF6))
    dash = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left + 0.15),
        Inches(top + 0.15),
        Inches(width - 0.3),
        Inches(height - 0.3),
    )
    dash.fill.background()
    dash.line.color.rgb = MUTED

    path = BUKTI / filename
    if path.exists():
        slide.shapes.add_picture(
            str(path), Inches(left + 0.2), Inches(top + 0.2), width=Inches(width - 0.4)
        )
        return

    tb = slide.shapes.add_textbox(
        Inches(left + 0.3), Inches(top + height / 2 - 0.55), Inches(width - 0.6), Inches(1.2)
    )
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run(p, "📸 SLOT SCREENSHOT", 14, True, MUTED)
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    run(p2, label, 12, False, INK)
    p3 = tf.add_paragraph()
    p3.alignment = PP_ALIGN.CENTER
    run(p3, f"Simpan sebagai: bukti/{filename}", 11, False, MUTED)


def blank(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(s)
    return s


def step_slide(prs, num, title, perintah, penjelasan, ss_file, ss_label, page):
    s = blank(prs)
    header(s, f"{num} · {title}", "Urutan demo presentasi")
    meaning_box(s, 0.4, 1.4, 6.2, 2.6, "Perintah", perintah, BLUE)
    meaning_box(s, 0.4, 4.2, 6.2, 2.6, "Penjelasan / hasil diharapkan", penjelasan, GREEN)
    ss_slot(s, 6.9, 1.4, 6.0, 5.4, ss_label, ss_file)
    footer(s, page)
    return s


def build():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # ----- 1 COVER -----
    s = blank(prs)
    hero = card(s, 1.2, 1.35, 10.9, 4.6)
    tf = hero.text_frame
    tf.clear()
    lines = [
        ("PRESENTASI UJI SISTEM IoT", 14, MUTED, False),
        ("Hardware ESP32 + DHT + LED", 28, INK, True),
        ("MQTT (Mosquitto) → Laravel 11 → MySQL", 18, MUTED, False),
        ("", 8, MUTED, False),
        ("Flow Uji End-to-End", 16, GREEN, True),
        ("Asesi: (isi nama & NIM)", 16, INK, False),
        ("PHP 8.2 · Laravel 11 · tanpa Flutter / simulator", 13, MUTED, False),
    ]
    first = True
    for text, size, color, bold in lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = PP_ALIGN.CENTER
        run(p, text, size, bold, color)
        p.space_after = Pt(6)
    footer(s, "1/14")

    # ----- 2 PETA -----
    s = blank(prs)
    header(s, "Peta Presentasi / Flow Uji", "Ikuti nomor urut saat demo di depan asesor")
    topics = [
        ("01", "Persiapan", "MySQL + Mosquitto + .env", BLUE),
        ("02", "Laravel serve", "API + dashboard :8000", BLUE),
        ("03", "mqtt:listen", "Subscriber → MySQL", GREEN),
        ("04", "ESP32 firmware", "DHT + LED + MQTT", PINK),
        ("05", "Bukti data", "Serial + listen + DB", GREEN),
        ("06", "Debug & OTA", "listen off · token · OTA", YELLOW),
    ]
    for i, (num, title, desc, color) in enumerate(topics):
        col = i % 3
        row = i // 3
        left = 0.5 + col * 4.2
        top = 1.55 + row * 2.5
        card(s, left, top, 3.9, 2.2)
        badge = s.shapes.add_shape(
            MSO_SHAPE.OVAL, Inches(left + 0.25), Inches(top + 0.4), Inches(0.7), Inches(0.7)
        )
        badge.fill.solid()
        badge.fill.fore_color.rgb = color
        badge.line.fill.background()
        bt = badge.text_frame
        bt.paragraphs[0].alignment = PP_ALIGN.CENTER
        run(bt.paragraphs[0], num, 12, True, WHITE)
        tb = s.shapes.add_textbox(Inches(left + 1.1), Inches(top + 0.45), Inches(2.5), Inches(1.4))
        tf = tb.text_frame
        tf.word_wrap = True
        run(tf.paragraphs[0], title, 18, True, INK)
        p2 = tf.add_paragraph()
        run(p2, desc, 13, False, MUTED)
    footer(s, "2/14")

    # ----- 3 OPENING -----
    s = blank(prs)
    header(s, "Opening — Apa yang dibangun?", "Naskah singkat ±1 menit")
    meaning_box(
        s,
        0.45,
        1.5,
        6.1,
        5.2,
        "Isi proyek (ingat urutan)",
        [
            "• Hardware: ESP32 + DHT11 + LED merah/hijau/kuning",
            "• Broker: Eclipse Mosquitto (MQTT port 1883)",
            "• Backend: Laravel 11 + MySQL",
            "• Subscriber: php artisan mqtt:listen",
            "• Monitor: Dashboard Blade (tanpa Flutter)",
            "• OTA: firmware v1 → v2 via MQTT command",
            "",
            "Kalimat pembuka:",
            "“Saya buat pemantauan suhu dengan ESP32,",
            "data dikirim MQTT ke Mosquitto, Laravel",
            "menyimpan ke MySQL, dipantau di dashboard,",
            "bisa OTA tanpa USB.”",
        ],
        BLUE,
    )
    meaning_box(
        s,
        6.8,
        1.5,
        6.0,
        5.2,
        "Beda dengan project Flutter",
        [
            "Project ini lebih simple:",
            "• Tidak pakai Flutter",
            "• Tidak pakai simulator Python",
            "• Telemetry murni dari hardware MQTT",
            "",
            "Yang wajib dibuktikan:",
            "1. Sensor + LED hidup",
            "2. MQTT connected + data ≥ beberapa baris",
            "3. Dashboard update",
            "4. Token ditolak jika salah",
            "5. OTA v1 → v2 (SOP)",
            "",
            "Token: iot-simple-token-2026",
            "DB: iot_simple_laravel",
        ],
        GREEN,
    )
    footer(s, "3/14")

    # ----- 4 ARSITEKTUR -----
    s = blank(prs)
    header(s, "Arsitektur Sistem", "Mosquitto = kurir · mqtt:listen = pencatat DB")
    boxes = [
        (0.4, "ESP32", "DHT + LED\npublish MQTT", PINK),
        (3.5, "Mosquitto", "Broker :1883\nteruskan pesan", BLUE),
        (6.6, "mqtt:listen", "Cek token\nsimpan MySQL", GREEN),
        (9.7, "Dashboard", "Grafik live\nhttp://…:8000", BLUE),
    ]
    for left, title, body, color in boxes:
        card(s, left, 1.8, 2.9, 2.7)
        topbar = s.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(left), Inches(1.8), Inches(2.9), Inches(0.55)
        )
        topbar.fill.solid()
        topbar.fill.fore_color.rgb = color
        topbar.line.fill.background()
        ttf = topbar.text_frame
        ttf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run(ttf.paragraphs[0], title, 14, True, WHITE)
        bb = s.shapes.add_textbox(Inches(left + 0.2), Inches(2.55), Inches(2.5), Inches(1.6))
        bb.text_frame.word_wrap = True
        first = True
        for line in body.split("\n"):
            p = bb.text_frame.paragraphs[0] if first else bb.text_frame.add_paragraph()
            first = False
            p.alignment = PP_ALIGN.CENTER
            run(p, line, 14, False, INK)
    for left in (3.15, 6.25, 9.35):
        a = s.shapes.add_textbox(Inches(left), Inches(2.85), Inches(0.4), Inches(0.4))
        a.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        run(a.text_frame.paragraphs[0], "→", 22, True, MUTED)

    meaning_box(
        s,
        0.4,
        4.85,
        12.5,
        1.95,
        "Cara baca (penting untuk presentasi)",
        [
            "ESP32 tidak tulis MySQL langsung. Mosquitto tidak simpan database.",
            "Tanpa php artisan mqtt:listen → Serial ESP tetap OK, dashboard tidak nambah data.",
            "HTTP di ESP hanya untuk unduh OTA (.bin), bukan telemetry.",
        ],
        MUTED,
    )
    footer(s, "4/14")

    # ----- 5 PERSIAPAN -----
    s = blank(prs)
    header(s, "0 · Persiapan sebelum demo", "Service & konfigurasi sekali jalan")
    meaning_box(
        s,
        0.4,
        1.4,
        6.2,
        5.4,
        "Checklist",
        [
            "1. Laragon → MySQL Start",
            "2. DB: iot_simple_laravel + php artisan migrate",
            "3. Mosquitto Broker → Running",
            "4. mosquitto.conf:",
            "     listener 1883 0.0.0.0",
            "     allow_anonymous true",
            "5. Firewall port 1883 (jika perlu)",
            "6. Uji: mosquitto_pub -h IP_PC (bukan hanya 127.0.0.1)",
            "7. config.h ESP: WIFI + MQTT_HOST = IP PC",
            "8. API_TOKEN sama dengan .env IOT_API_TOKEN",
            "",
            "PHP teman: 8.2.x OK (Laravel 11)",
        ],
        BLUE,
    )
    ss_slot(
        s,
        6.9,
        1.4,
        6.0,
        5.4,
        "SS services.msc Mosquitto Running\n+ ipconfig IPv4 PC",
        "debug/01_persiapan_mosquitto_ip.png",
    )
    footer(s, "5/14")

    # ----- 6 LARAVEL -----
    step_slide(
        prs,
        "1",
        "Jalankan Laravel",
        [
            "cd ...\\platform\\laravel",
            "composer install   # sekali saja",
            "php artisan serve --host=0.0.0.0 --port=8000",
            "",
            "Cek browser:",
            "http://127.0.0.1:8000/api/health",
            "http://127.0.0.1:8000/",
        ],
        [
            "Health → \"status\":\"ok\"",
            "Dashboard terbuka (mungkin masih kosong)",
            "Terminal serve tetap hidup selama demo",
            "",
            "Ini API + UI saja.",
            "Belum menyimpan data MQTT",
            "sampai mqtt:listen jalan.",
        ],
        "dashboard/01_health_atau_serve.png",
        "SS terminal artisan serve\n+ browser /api/health",
        "6/14",
    )

    # ----- 7 MQTT LISTEN -----
    step_slide(
        prs,
        "2",
        "Jalankan subscriber mqtt:listen",
        [
            "cd ...\\platform\\laravel",
            "php artisan mqtt:listen",
            "",
            "Harus muncul:",
            "=== Laravel MQTT Subscriber ===",
            "Broker : 127.0.0.1:1883",
            "Menunggu pesan dari ESP32...",
        ],
        [
            "Ini proses pencatat MQTT → MySQL",
            "File: MqttListenCommand.php",
            "Config token/host: .env + config/iot.php",
            "",
            "Kalau terminal ini dimatikan:",
            "ESP tetap publish OK,",
            "dashboard tidak nambah baris.",
            "",
            "Log sukses: [DB] tersimpan id=...",
        ],
        "mqtt_listen/01_mqtt_listen_ready.png",
        "SS terminal mqtt:listen siap",
        "7/14",
    )

    # ----- 8 ESP32 -----
    step_slide(
        prs,
        "3",
        "Upload & jalankan ESP32",
        [
            "Arduino: buka firmware/v1/dht_rgb_iot.ino",
            "Edit config.h → WIFI + MQTT_HOST=IP PC",
            "Upload · Serial Monitor 115200",
            "",
            "Wiring LED:",
            "25 merah · 26 hijau · 27 kuning",
            "DHT DATA → GPIO 4",
        ],
        [
            "Serial yang diharapkan:",
            "[WIFI] connected + IP ESP",
            "[MQTT] connected",
            "[DHT] temp=.. hum=..",
            "[TEL] MQTT ... OK",
            "",
            "LED: satu warna per rentang suhu",
            "v1: <25 hijau | 25–30 kuning | >30 merah",
            "",
            "rc=-2 → Mosquitto belum listen LAN",
        ],
        "serial/01_esp32_mqtt_ok.png",
        "SS Serial Monitor MQTT connected",
        "8/14",
    )

    # ----- 9 BUKTI DATA -----
    s = blank(prs)
    header(s, "4 · Bukti data masuk (tiga sisi)", "Serial + mqtt:listen + Dashboard/MySQL")
    ss_slot(s, 0.35, 1.35, 4.1, 3.5, "Serial [TEL] OK", "serial/02_telemetry_ok.png")
    ss_slot(s, 4.6, 1.35, 4.1, 3.5, "mqtt:listen [DB] tersimpan", "mqtt_listen/02_db_tersimpan.png")
    ss_slot(s, 8.85, 1.35, 4.1, 3.5, "Dashboard grafik hidup", "dashboard/02_dashboard_live.png")
    meaning_box(
        s,
        0.35,
        5.05,
        12.6,
        1.8,
        "Apa yang dibuktikan?",
        [
            "End-to-end: hardware → MQTT → Laravel → MySQL → UI.",
            "Kolom source di DB = mqtt. Firmware field fw = 1.0.0 (sebelum OTA).",
            "Cek MySQL opsional: SELECT id,temp,hum,seq,source,fw FROM telemetries ORDER BY id DESC LIMIT 5;",
        ],
        GREEN,
    )
    footer(s, "9/14")

    # ----- 10 DEBUG LISTEN OFF -----
    step_slide(
        prs,
        "5",
        "Debugging: matikan mqtt:listen",
        [
            "Di terminal mqtt:listen → Ctrl+C",
            "Biarkan Mosquitto + ESP tetap hidup",
            "",
            "Opsional bukti broker masih dapat pesan:",
            "mosquitto_sub -h 127.0.0.1 -t",
            '  "smarthome/esp32-dht-rgb-01/telemetry" -v',
        ],
        [
            "Serial ESP: tetap [TEL] ... OK",
            "LED: tetap ikut suhu",
            "Dashboard: tidak nambah data baru",
            "",
            "Artinya: Mosquitto ≠ database.",
            "Subscriber Laravel wajib untuk simpan.",
            "",
            "Nyalakan lagi: php artisan mqtt:listen",
        ],
        "debug/02_listen_off_serial_ok.png",
        "SS Serial tetap OK\nsaat listen dimatikan",
        "10/14",
    )

    # ----- 11 TOKEN -----
    step_slide(
        prs,
        "6",
        "Debugging: token salah / ditolak",
        [
            "Sementara ubah API_TOKEN di ESP",
            "(atau IOT_API_TOKEN di .env) agar beda",
            "Upload / restart listen",
            "",
            "Kembalikan token sama setelah demo:",
            "iot-simple-token-2026",
        ],
        [
            "mqtt:listen menampilkan:",
            "Token invalid/missing — data ditolak",
            "",
            "DB tidak bertambah",
            "",
            "Lokasi config:",
            "· .env → IOT_API_TOKEN",
            "· config/iot.php",
            "· MqttListenCommand.php (cek hash_equals)",
            "· firmware config.h → API_TOKEN",
        ],
        "mqtt_listen/03_token_reject.png",
        "SS terminal Token invalid",
        "11/14",
    )

    # ----- 12 OTA -----
    step_slide(
        prs,
        "7",
        "OTA firmware v1 → v2",
        [
            "1. Compile v2 → Export compiled Binary",
            "2. Salin .bin ke:",
            "   storage/app/ota/firmware_v2.bin",
            "3. Laravel serve harus hidup",
            "4. Mosquitto:",
            "mosquitto_pub -h 127.0.0.1 \\",
            '  -t "smarthome/esp32-dht-rgb-01/command" \\',
            '  -m "{\\"action\\":\\"ota_update\\",\\"token\\":\\"iot-simple-token-2026\\"}"',
        ],
        [
            "Serial: [OTA] Authorized... → reboot",
            "Setelah reboot: fw 2.0.0",
            "Interval 3 detik (lebih cepat)",
            "LED rule lebih ketat (<24 / 24–28 / >28)",
            "",
            "Tanpa token → [SEC] REJECT di ESP",
            "Detail: docs/03_sop_ota.md",
        ],
        "ota/01_ota_serial.png",
        "SS Serial OTA sukses / fw 2.0.0",
        "12/14",
    )

    # ----- 13 RINGKAS FLOW -----
    s = blank(prs)
    header(s, "Ringkas flow presentasi", "Hafalkan 8 langkah ini")
    steps = [
        ("01", "MySQL + Mosquitto Start"),
        ("02", "php artisan serve"),
        ("03", "php artisan mqtt:listen"),
        ("04", "ESP32 Serial MQTT OK"),
        ("05", "Dashboard data hidup"),
        ("06", "Debug: listen off"),
        ("07", "Debug: token tolak"),
        ("08", "OTA v1 → v2"),
    ]
    for i, (num, text) in enumerate(steps):
        col = i % 4
        row = i // 4
        left = 0.45 + col * 3.2
        top = 1.55 + row * 2.4
        card(s, left, top, 3.0, 2.1)
        badge = s.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left + 0.2), Inches(top + 0.35), Inches(0.7), Inches(0.45)
        )
        badge.fill.solid()
        badge.fill.fore_color.rgb = GREEN if i < 5 else YELLOW
        badge.line.fill.background()
        bp = badge.text_frame.paragraphs[0]
        bp.alignment = PP_ALIGN.CENTER
        run(bp, num, 12, True, WHITE)
        tb = s.shapes.add_textbox(Inches(left + 0.2), Inches(top + 1.0), Inches(2.6), Inches(0.8))
        tb.text_frame.word_wrap = True
        run(tb.text_frame.paragraphs[0], text, 14, True, INK)
    footer(s, "13/14")

    # ----- 14 CLOSING + SS GUIDE -----
    s = blank(prs)
    header(s, "Penutup + panduan isi screenshot", "Teman asesi yang mengambil SS")
    meaning_box(
        s,
        0.4,
        1.4,
        6.2,
        5.4,
        "Kalimat penutup",
        [
            "“Demikian demo end-to-end:",
            "hardware ESP32 mengirim MQTT,",
            "Laravel subscriber menyimpan MySQL,",
            "dashboard memantau, keamanan token,",
            "dan OTA v1 ke v2.”",
            "",
            "Siap jawab:",
            "· Kenapa butuh mqtt:listen?",
            "· rc=-2 artinya apa?",
            "· LED logic merah/hijau/kuning?",
            "· Token dikonfigurasi di mana?",
        ],
        GREEN,
    )
    meaning_box(
        s,
        6.9,
        1.4,
        6.0,
        5.4,
        "Isi SS di folder bukti/",
        [
            "debug/01_persiapan_mosquitto_ip.png",
            "dashboard/01_health_atau_serve.png",
            "mqtt_listen/01_mqtt_listen_ready.png",
            "serial/01_esp32_mqtt_ok.png",
            "serial/02_telemetry_ok.png",
            "mqtt_listen/02_db_tersimpan.png",
            "dashboard/02_dashboard_live.png",
            "debug/02_listen_off_serial_ok.png",
            "mqtt_listen/03_token_reject.png",
            "ota/01_ota_serial.png",
            "",
            "Lalu: python buat_ppt_presentasi.py",
            "atau tempel manual ke slot 📸",
        ],
        BLUE,
    )
    footer(s, "14/14")

    prs.save(str(OUT))
    print(f"OK → {OUT}")


if __name__ == "__main__":
    build()
