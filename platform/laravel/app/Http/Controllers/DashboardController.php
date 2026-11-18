<?php

namespace App\Http\Controllers;

use App\Models\Telemetry;
use Illuminate\View\View;

class DashboardController extends Controller
{
    public function index(): View
    {
        $last = Telemetry::query()->latest('id')->first();
        $online = $last ? $last->created_at->gt(now()->subSeconds(20)) : false;
        $series = Telemetry::query()
            ->latest('id')
            ->limit(40)
            ->get()
            ->reverse()
            ->values();

        return view('dashboard', [
            'deviceId' => config('iot.device_id'),
            'topic' => config('iot.topic_telemetry'),
            'online' => $online,
            'total' => Telemetry::count(),
            'last' => $last,
            'series' => $series,
            'apiBase' => url('/api'),
            'token' => config('iot.api_token'),
        ]);
    }
}
