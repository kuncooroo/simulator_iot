<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>DHT + RGB Monitor · Laravel</title>
    <link rel="preconnect" href="https://fonts.bunny.net">
    <link href="https://fonts.bunny.net/css?family=dm-sans:400,500,600,700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.min.js"></script>
    <style>
        :root {
            --bg: #0f1720;
            --surface: #182230;
            --ink: #e8eef6;
            --muted: #8fa0b3;
            --line: #2a3a4d;
            --accent: #3ecf8e;
            --warn: #f0b429;
            --danger: #ef5f5f;
            --blue: #5b9fd4;
        }
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: "DM Sans", system-ui, sans-serif;
            background:
                radial-gradient(ellipse at 10% 0%, rgba(62, 207, 142, 0.12), transparent 45%),
                radial-gradient(ellipse at 90% 20%, rgba(91, 159, 212, 0.10), transparent 40%),
                var(--bg);
            color: var(--ink);
            min-height: 100vh;
        }
        .wrap { max-width: 1080px; margin: 0 auto; padding: 28px 18px 48px; }
        .top { display: flex; justify-content: space-between; gap: 16px; align-items: flex-start; margin-bottom: 22px; }
        h1 { margin: 0; font-size: 1.7rem; letter-spacing: -0.02em; }
        .sub { margin: 6px 0 0; color: var(--muted); font-size: 0.95rem; }
        .badge {
            display: inline-flex; align-items: center; gap: 8px;
            padding: 10px 14px; border-radius: 999px;
            background: var(--surface); border: 1px solid var(--line);
            font-weight: 700; font-size: 13px;
        }
        .dot { width: 9px; height: 9px; border-radius: 50%; background: var(--danger); }
        .dot.on { background: var(--accent); box-shadow: 0 0 0 4px rgba(62, 207, 142, 0.2); }
        .grid { display: grid; gap: 14px; grid-template-columns: repeat(12, 1fr); }
        .card {
            background: var(--surface); border: 1px solid var(--line);
            border-radius: 16px; padding: 16px 18px;
        }
        .kpi { grid-column: span 3; }
        .chart { grid-column: span 8; }
        .side { grid-column: span 4; }
        .log { grid-column: span 12; }
        @media (max-width: 900px) {
            .kpi, .chart, .side, .log { grid-column: span 12; }
            .top { flex-direction: column; }
        }
        .label { color: var(--muted); font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; }
        .value { margin-top: 8px; font-size: 1.7rem; font-weight: 700; }
        .meta { margin-top: 4px; color: var(--muted); font-size: 0.85rem; }
        table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
        th, td { padding: 8px 6px; border-bottom: 1px solid var(--line); text-align: left; }
        th { color: var(--muted); font-weight: 600; font-size: 12px; }
        .actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
        button {
            border: 0; border-radius: 10px; padding: 10px 14px;
            background: var(--accent); color: #062216; font-weight: 700; cursor: pointer;
        }
        button.secondary { background: #243447; color: var(--ink); }
        button.warn { background: var(--warn); color: #2a1f00; }
        pre {
            margin: 10px 0 0; padding: 10px; border-radius: 10px;
            background: #101820; color: #b7c6d6; font-size: 12px;
            overflow: auto; max-height: 160px;
        }
    </style>
</head>
<body>
<div class="wrap">
    <div class="top">
        <div>
            <h1>DHT + RGB IoT Monitor</h1>
            <p class="sub">Laravel + MySQL · Device <strong>{{ $deviceId }}</strong> · Topic <code>{{ $topic }}</code></p>
        </div>
        <div class="badge">
            <span class="dot {{ $online ? 'on' : '' }}"></span>
            {{ $online ? 'ONLINE' : 'OFFLINE' }}
        </div>
    </div>

    <div class="grid">
        <div class="card kpi">
            <div class="label">Suhu</div>
            <div class="value" id="temp">{{ $last?->temp !== null ? number_format($last->temp, 1).'°C' : '—' }}</div>
            <div class="meta">FW {{ $last->fw ?? '—' }}</div>
        </div>
        <div class="card kpi">
            <div class="label">Kelembapan</div>
            <div class="value" id="hum">{{ $last?->hum !== null ? number_format($last->hum, 1).'%' : '—' }}</div>
            <div class="meta">Source {{ $last->source ?? '—' }}</div>
        </div>
        <div class="card kpi">
            <div class="label">Seq</div>
            <div class="value" id="seq">{{ $last->seq ?? '—' }}</div>
            <div class="meta">Total {{ $total }}</div>
        </div>
        <div class="card kpi">
            <div class="label">OTA</div>
            <div class="value" style="font-size:1.1rem;">v1 → v2</div>
            <div class="meta"><a href="{{ $apiBase }}/ota/info" style="color:var(--blue)">/api/ota/info</a></div>
        </div>

        <div class="card chart">
            <div class="label">Grafik suhu & kelembapan</div>
            <canvas id="chart" height="120"></canvas>
        </div>

        <div class="card side">
            <div class="label">Aksi cepat</div>
            <div class="actions">
                <button type="button" onclick="refreshStatus()">Refresh</button>
                <button type="button" class="secondary" onclick="sendPing()">Ping command</button>
                <button type="button" class="warn" onclick="triggerOta()">Trigger OTA</button>
            </div>
            <pre id="log">Siap. Auto-refresh tiap 3 detik.</pre>
        </div>

        <div class="card log">
            <div class="label">Data terbaru</div>
            <table>
                <thead>
                <tr>
                    <th>ID</th><th>Temp</th><th>Hum</th><th>Seq</th><th>FW</th><th>Source</th><th>Waktu</th>
                </tr>
                </thead>
                <tbody id="rows">
                @forelse($series->reverse() as $row)
                    <tr>
                        <td>{{ $row->id }}</td>
                        <td>{{ number_format($row->temp, 1) }}</td>
                        <td>{{ number_format($row->hum, 1) }}</td>
                        <td>{{ $row->seq }}</td>
                        <td>{{ $row->fw }}</td>
                        <td>{{ $row->source }}</td>
                        <td>{{ $row->created_at }}</td>
                    </tr>
                @empty
                    <tr><td colspan="7">Belum ada data. Pastikan ESP32 + Mosquitto + <code>php artisan mqtt:listen</code> sudah jalan.</td></tr>
                @endforelse
                </tbody>
            </table>
        </div>
    </div>
</div>

<script>
const API = @json($apiBase);
const TOKEN = @json($token);
const initialSeries = @json($series);

const ctx = document.getElementById('chart');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: initialSeries.map(x => x.seq),
        datasets: [
            { label: 'Temp °C', data: initialSeries.map(x => x.temp), borderColor: '#ef5f5f', tension: 0.25 },
            { label: 'Hum %', data: initialSeries.map(x => x.hum), borderColor: '#5b9fd4', tension: 0.25 },
        ]
    },
    options: {
        responsive: true,
        plugins: { legend: { labels: { color: '#8fa0b3' } } },
        scales: {
            x: { ticks: { color: '#8fa0b3' }, grid: { color: '#2a3a4d' } },
            y: { ticks: { color: '#8fa0b3' }, grid: { color: '#2a3a4d' } },
        }
    }
});

function log(msg) {
    const el = document.getElementById('log');
    const t = new Date().toLocaleTimeString();
    el.textContent = `[${t}] ${msg}\n` + el.textContent.split('\n').slice(0, 8).join('\n');
}

async function refreshStatus() {
    try {
        const [st, latest] = await Promise.all([
            fetch(API + '/telemetry/status').then(r => r.json()),
            fetch(API + '/telemetry/latest?limit=40').then(r => r.json()),
        ]);
        document.getElementById('temp').textContent = st.last ? st.last.temp.toFixed(1) + '°C' : '—';
        document.getElementById('hum').textContent = st.last ? st.last.hum.toFixed(1) + '%' : '—';
        document.getElementById('seq').textContent = st.last ? st.last.seq : '—';
        document.querySelector('.dot').classList.toggle('on', !!st.online);
        document.querySelector('.badge').lastChild.textContent = st.online ? ' ONLINE' : ' OFFLINE';

        const items = (latest.items || []).slice().reverse();
        chart.data.labels = items.map(x => x.seq);
        chart.data.datasets[0].data = items.map(x => x.temp);
        chart.data.datasets[1].data = items.map(x => x.hum);
        chart.update('none');

        const rows = document.getElementById('rows');
        rows.innerHTML = items.slice().reverse().map(r => `
            <tr>
                <td>${r.id}</td>
                <td>${Number(r.temp).toFixed(1)}</td>
                <td>${Number(r.hum).toFixed(1)}</td>
                <td>${r.seq}</td>
                <td>${r.fw}</td>
                <td>${r.source}</td>
                <td>${r.created_at}</td>
            </tr>
        `).join('') || '<tr><td colspan="7">Belum ada data. Nyalakan ESP32 + Mosquitto + mqtt:listen.</td></tr>';
    } catch (e) {
        log('Refresh gagal: ' + e.message);
    }
}

async function sendPing() {
    const res = await fetch(API + '/command', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-API-Token': TOKEN,
        },
        body: JSON.stringify({ action: 'ping', note: 'dashboard' }),
    });
    const data = await res.json();
    log('Ping → HTTP ' + res.status + ' ' + JSON.stringify(data));
}

async function triggerOta() {
    const res = await fetch(API + '/command', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-API-Token': TOKEN,
        },
        body: JSON.stringify({ action: 'ota_update', note: 'dashboard trigger' }),
    });
    const data = await res.json();
    log('OTA command → HTTP ' + res.status + ' ' + JSON.stringify(data));
    log('Catatan: ESP32 butuh perintah MQTT ota_update agar benar-benar update.');
}

setInterval(refreshStatus, 3000);
</script>
</body>
</html>
