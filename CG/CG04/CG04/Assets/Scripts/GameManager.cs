using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class GameManager : MonoBehaviour
{
    public GameObject menuCanvas;
    public GameObject gameOverCanvas;
    public GameObject inGameUI;
    public Text scoreText;
    public Text difficultyText;
    public Flight bird;
    public PipeSpawner pipeSpawner;
    private int score = 0;
    private string difficulty = "normal";

    public void IncrementScore(int inc = 1)
    {
        score += inc;
    }

    public int GetScore()
    {
        return score;
    }

    public void GameOver()
    {
        inGameUI.SetActive(false);
        gameOverCanvas.SetActive(true);
        Time.timeScale = 0;
    }

    // Start is called before the first frame update
    void Start()
    {
        Time.timeScale = 0;
        inGameUI.SetActive(false);
        gameOverCanvas.SetActive(false);
        menuCanvas.SetActive(true);
    }

    // Update is called once per frame
    void Update()
    {
        scoreText.text = score.ToString();
    }

    public void ShowMenu()
    {
        inGameUI.SetActive(false);
        gameOverCanvas.SetActive(false);
        menuCanvas.SetActive(true);
    }

    public void StartGame()
    {
        score = 0;

        bird.ResetPosition();
        pipeSpawner.DeleteAllPipes();

        menuCanvas.SetActive(false);
        gameOverCanvas.SetActive(false);
        inGameUI.SetActive(true);

        if (difficulty == "normal")
            Time.timeScale = 50F;
        else if (difficulty == "hard")
            Time.timeScale = 1;
        else if (difficulty == "easy")
            Time.timeScale = 0.6F;

    }

    public void ChangeDifficulty()
    {
        if (difficulty == "normal")
            difficulty = "hard";

        else if (difficulty == "hard")
            difficulty = "easy";

        else if (difficulty == "easy")
            difficulty = "normal";

        difficultyText.text = difficulty;
    }
}
