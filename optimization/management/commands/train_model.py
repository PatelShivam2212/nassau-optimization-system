from django.core.management.base import BaseCommand
from optimization.services.ml_service import MLService


class Command(BaseCommand):
    help = 'Trains the Lead Time prediction model'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting model training...")
        ml = MLService()
        metrics = ml.train_model()

        if isinstance(metrics, dict):
            self.stdout.write(self.style.SUCCESS(f"Model Trained Successfully!"))
            self.stdout.write(f"R2 Score: {metrics['R2']:.4f}")
            self.stdout.write(f"MAE: {metrics['MAE']:.2f} days")
        else:
            self.stdout.write(self.style.ERROR(metrics))