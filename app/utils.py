from app.storage import users
import matplotlib.pyplot as plt

def calculate_goals(weight, height, age, activity, temperature):
    water = weight * 30 + (500 if activity > 30 else 0) + (500 if temperature > 25 else 0)
    calories = 10 * weight + 6.25 * height - 5 * age + activity * 5
    return {"water_goal": water, "calorie_goal": calories}

def get_user_data(user_id):
    user = users.get(user_id)
    if not user:
        raise ValueError("Сначала настройте профиль с помощью команды /set_profile.")
    return user

def generate_progress_graph(user_data, file_path="progress.png"):
    try:
        water_goal = user_data["water_goal"] + user_data.get("extra_water", 0)
        logged_water = user_data.get("logged_water", 0)

        calorie_goal = user_data["calorie_goal"] + user_data.get("extra_calories", 0)
        burned_calories = user_data.get("burned_calories", 0)
        updated_calorie_goal = calorie_goal + burned_calories
        logged_calories = user_data.get("logged_calories", 0)

        water_progress_percent = min((logged_water / water_goal) * 100, 100)
        calorie_progress_percent = min((logged_calories / updated_calorie_goal) * 100, 100)

        plt.style.use("ggplot")
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        axes[0].bar(
            ["Прогресс", "Цель"],
            [logged_water, water_goal],
            color=["dodgerblue", "limegreen"],
            edgecolor="black",
        )
        axes[0].set_title("Прогресс по воде", fontsize=14, fontweight="bold")
        axes[0].set_ylabel("Количество (мл)", fontsize=12)
        axes[0].set_ylim(0, max(water_goal, logged_water) * 1.2)
        axes[0].grid(axis="y", linestyle="--", alpha=0.7)
        axes[0].text(
            0,
            logged_water + max(water_goal, logged_water) * 0.05,
            f"{water_progress_percent:.1f}%",
            ha="center",
            fontsize=12,
            color="black",
            fontweight="bold",
        )

        axes[1].bar(
            ["Прогресс", "Цель"],
            [logged_calories, updated_calorie_goal],
            color=["orange", "limegreen"],
            edgecolor="black",
        )
        axes[1].set_title("Прогресс по калориям", fontsize=14, fontweight="bold")
        axes[1].set_ylabel("Количество (ккал)", fontsize=12)
        axes[1].set_ylim(0, max(updated_calorie_goal, logged_calories) * 1.2)
        axes[1].grid(axis="y", linestyle="--", alpha=0.7)
        axes[1].text(
            0,
            logged_calories + max(updated_calorie_goal, logged_calories) * 0.05,
            f"{calorie_progress_percent:.1f}%",
            ha="center",
            fontsize=12,
            color="black",
            fontweight="bold",
        )

        for ax in axes:
            ax.set_xticks([0, 1])
            ax.set_xticklabels(["Прогресс", "Цель"], fontsize=12)

        plt.tight_layout()
        plt.savefig(file_path, dpi=300)
        plt.close()
    except Exception as e:
        print(f"Ошибка при создании графика: {e}")
        raise