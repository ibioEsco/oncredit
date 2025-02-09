
import boto3

session = boto3.Session(profile_name='default') 
client = session.client('rekognition')

def create_session():

    response = client.create_face_liveness_session()
    
    session_id = response.get("SessionId")
    print('SessionId: ' + session_id)

    return session_id
    
    
def get_session_results(session_id):

    response = client.get_face_liveness_session_results(SessionId=session_id)
    
    confidence = response.get("Confidence")
    status = response.get("Status")
    
    # print('Confidence: ' + "{:.2f}".format(confidence) + "%")
    print(confidence)
    print('Status: ' + status)
    
    return status


def main():
    session_id = create_session()
    print('Created a Face Liveness Session with ID: ' + session_id)
    
    status = get_session_results(session_id)
    print('Status of Face Liveness Session: ' + status)
        

if __name__ == "__main__":
    main()

                    