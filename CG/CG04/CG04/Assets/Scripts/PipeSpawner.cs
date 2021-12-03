using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PipeSpawner : MonoBehaviour
{
    public float maxTime = 1;
    private float timer = 0;
    public GameObject pipe;
    public float maxHeight = 0.5F;
    public float minHeight = -0.3F;
    public float minInterval = 0.2F;
    public float maxInterval = 0.05F;

    Queue<GameObject> spawnedPipes = new Queue<GameObject>();


    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        if (timer > maxTime)
        {
            GameObject newPipe = Instantiate(pipe);

            GameObject newPipeUpper = newPipe.transform.GetChild(0).gameObject;
            GameObject newPipeLower = newPipe.transform.GetChild(1).gameObject;

            newPipe.transform.position = transform.position + new Vector3(0, Random.Range(minHeight, maxHeight), 0);

            float pipeSpread = Random.Range(minInterval, maxInterval);
            newPipeUpper.transform.position = newPipeUpper.transform.position + new Vector3(0, pipeSpread, 0);
            newPipeLower.transform.position = newPipeLower.transform.position + new Vector3(0, -pipeSpread, 0);

            spawnedPipes.Enqueue(newPipe);

            if (spawnedPipes.Count > 15)
            {
                GameObject toDestroy = spawnedPipes.Dequeue();
                Destroy(toDestroy, 0);
            }

            timer = 0;
        }

        timer += Time.deltaTime;
    }

    public void DeleteAllPipes()
    {
        GameObject toDestroy;
        while (!(spawnedPipes.Count == 0))
        {
            toDestroy = spawnedPipes.Dequeue();
            Destroy(toDestroy, 0);
        }
    }
}
