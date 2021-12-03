using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Flight : MonoBehaviour
{
    public GameManager gameManager;
    public float velocity = 1.4F;
    public Vector3 basePosition = new Vector3(0, 1, 0);
    private Rigidbody2D rigidBody;

    // Start is called before the first frame update
    void Start()
    {
        rigidBody = GetComponent<Rigidbody2D>();
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            // Jump
            rigidBody.velocity = Vector2.up * velocity;
        }
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        gameManager.GameOver();
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        gameManager.IncrementScore();
    }

    public void ResetPosition()
    {
        transform.position = basePosition;
    }
}
