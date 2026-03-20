from django.core.management.base import BaseCommand
from optimization.services.ml_service import MLService


class Command(BaseCommand):
    help = 'Trains the Lead Time prediction model'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting model training...")
        ml = MLService()
        metrics = ml.train_model()

        if isinstance(metrics, dict):
            self.stdout.write(self.style.SUCCESS("Model Trained Successfully!"))
            # Extract best model metrics
            best_metrics = metrics['all_results'][metrics['winner']]
            self.stdout.write(f"Winner: {metrics['winner']}")
            self.stdout.write(f"R2 Score: {best_metrics['R2']:.4f}")
            self.stdout.write(f"MAE: {best_metrics['MAE']:.2f} days")
            self.stdout.write(f"RMSE: {best_metrics['RMSE']:.2f} days")
        else:
            self.stdout.write(self.style.ERROR(metrics))