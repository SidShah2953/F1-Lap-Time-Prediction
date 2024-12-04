from sklearn.metrics import mean_absolute_error, r2_score
from helpers.misc import display_dict


def evaluate_model(y_true, y_pred, model_name):
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    display_dict(
                    {
                        "Mean Absolute Error": mae,
                        "R-squared Score": r2
                    },
                    title=f"{model_name} Metrics:"
                )