<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Telemetry;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class TelemetryController extends Controller
{
    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'device_id' => ['required', 'string', 'max:64'],
            'fw' => ['nullable', 'string', 'max:32'],
            'temp' => ['required', 'numeric'],
            'hum' => ['required', 'numeric'],
            'seq' => ['required', 'integer'],
            'ts' => ['nullable', 'integer'],
            'source' => ['nullable', 'string', 'max:16'],
            'token' => ['nullable', 'string'],
        ]);

        $row = Telemetry::create([
            'device_id' => $data['device_id'],
            'fw' => $data['fw'] ?? 'unknown',
            'temp' => $data['temp'],
            'hum' => $data['hum'],
            'seq' => $data['seq'],
            'device_ts' => $data['ts'] ?? null,
            'source' => $data['source'] ?? 'http',
        ]);

        return response()->json([
            'ok' => true,
            'stored' => $row,
        ], 201);
    }

    public function latest(Request $request): JsonResponse
    {
        $limit = max(1, min((int) $request->query('limit', 20), 200));
        $items = Telemetry::query()->latest('id')->limit($limit)->get();

        return response()->json([
            'count' => $items->count(),
            'items' => $items,
        ]);
    }

    public function status(): JsonResponse
    {
        $last = Telemetry::query()->latest('id')->first();
        $online = $last ? $last->created_at->gt(now()->subSeconds(20)) : false;

        return response()->json([
            'total_received' => Telemetry::count(),
            'last' => $last,
            'online' => $online,
            'device_id' => config('iot.device_id'),
            'topic_telemetry' => config('iot.topic_telemetry'),
        ]);
    }
}
