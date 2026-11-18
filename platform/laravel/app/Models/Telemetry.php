<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Telemetry extends Model
{
    protected $fillable = [
        'device_id',
        'fw',
        'temp',
        'hum',
        'seq',
        'device_ts',
        'source',
    ];

    protected $casts = [
        'temp' => 'float',
        'hum' => 'float',
        'seq' => 'integer',
        'device_ts' => 'integer',
    ];
}
