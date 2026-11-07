from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)
r1=client.post('/api/auth/login',json={'email':'creator@codenexus.demo','password':'creator123'})
tok_creator=r1.json()['access_token']
h_creator={'Authorization':f'Bearer {tok_creator}'}

r2=client.post('/api/drafts',json={
    'title':'New Product Launch Post',
    'content':'We leverage our unique synergy to provide an affordable cloud solution.',
    'channel':'social_post',
    'purpose':'Brand launch',
    'workspace_id':1
},headers=h_creator)
draft_id=r2.json()['id']
print('Created draft:',draft_id)

r3=client.post(f'/api/drafts/{draft_id}/review',headers=h_creator)
findings=r3.json()
print('Findings detected:',len(findings))
for f in findings:
    print(' *',f['category'],f['quoted_content'],'status:',f['status'])

aff_finding=next(f for f in findings if f['quoted_content']=='affordable')
r4=client.patch(f'/api/drafts/{draft_id}/findings/{aff_finding["id"]}',json={
    'action':'dispute',
    'dispute_reason':'Context is pricing comparison with market rates'
},headers=h_creator)
print('Disputed finding status:',r4.json()['status'],'reason:',r4.json()['dispute_reason'])

r5=client.post('/api/auth/login',json={'email':'manager@codenexus.demo','password':'manager123'})
tok_mgr=r5.json()['access_token']
h_mgr={'Authorization':f'Bearer {tok_mgr}'}

client.post(f'/api/drafts/{draft_id}/comments',json={'text':'Please rephrase affordable to specific tiers before final approval.'},headers=h_mgr)

r6=client.get(f'/api/drafts/{draft_id}',headers=h_mgr)
d_data=r6.json()
print('Comments on draft:',len(d_data.get('comments',[])))
print('Status:',d_data['status'])

r7=client.get('/api/insights/1',headers=h_mgr)
print('Insights:',r7.json())

