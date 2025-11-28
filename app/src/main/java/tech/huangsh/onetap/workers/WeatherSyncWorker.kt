package tech.huangsh.onetap.workers

import android.content.Context
import androidx.hilt.work.HiltWorker
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject
import tech.huangsh.onetap.data.repository.WeatherRepository

@HiltWorker
class WeatherSyncWorker @AssistedInject constructor(
    @Assisted context: Context,
    @Assisted workerParams: WorkerParameters,
    private val weatherRepository: WeatherRepository
) : CoroutineWorker(context, workerParams) {

    override suspend fun doWork(): Result {
        return try {
            weatherRepository.refreshWeather()
            Result.success()
        } catch (throwable: Exception) {
            Result.retry()
        }
    }

    companion object {
        const val UNIQUE_WORK_NAME = "weather_sync"
        const val ONE_TIME_WORK_NAME = "weather_sync_now"
    }
}
