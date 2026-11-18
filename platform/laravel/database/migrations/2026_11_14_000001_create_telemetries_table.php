<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('telemetries', function (Blueprint $table) {
            $table->id();
            $table->string('device_id', 64)->index();
            $table->string('fw', 32)->default('unknown');
            $table->float('temp');
            $table->float('hum');
            $table->unsignedBigInteger('seq')->index();
            $table->unsignedBigInteger('device_ts')->nullable();
            $table->string('source', 16)->default('http'); // http|mqtt|simulator
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('telemetries');
    }
};
