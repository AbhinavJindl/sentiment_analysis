import random 
import pickle
no_words = 5000
no_reviews = 1000
no_validation=1000
no_test=1000
forest_trees=50
forest_tree_features=2000



def add_noice(review_list_pos,review_list_neg,p):
	n=int((p/100)*len(review_list)/2)
	random.sample(review_list,n)

def load(filename):
	file = open(filename,'rb')
	obj=pickle.load(file)
	file.close()
	return obj

def save(obj,filename):
	file=open(filename,'wb')
	pickle.dump(obj,file)
	file.close()

#returns a dictionary for a review given string
def list_review(s,indexlist):
	dic = {}
	tokens=s.split(" ")
	dic['sentiment']=int(tokens[0])
	dic['list']=[]
	for i in range(1,len(tokens)):
		t=tokens[i].split(":")
		if int(t[0]) in indexlist:
			dic['list'].append(int(t[0]))
	return dic

def preprocess():
	wordsfile = open('aclImdb_v1/aclImdb/imdb.vocab','r',encoding='utf-8')
	valuefile = open('aclImdb_v1/aclImdb/imdbEr.txt','r',encoding='utf-8')


	count=0
	words_i=[]
	for line in valuefile:
		linetoken=line.split('\n')
		current=(count, float(linetoken[0]))
		words_i.append(current)
		count=count+1
	words_i= sorted(words_i,key=lambda x: x[1])
	indexlist=[]
	for i in range(int(no_words/2)):
		indexlist.append(words_i[i][0])
		indexlist.append(words_i[-i][0])
	indexlist= sorted(indexlist)

	forest_index_lists=[]

	for i in range(forest_trees):
		forest_index_lists.append(random.sample(indexlist,forest_tree_features))

	reviewsfile = open('aclImdb_v1/aclImdb/train/labeledBow.feat','r',encoding='utf-8')
	full_review_list = reviewsfile.readlines();
	random_list_pos = random.sample(range(0,int(len(full_review_list)/2)),int(no_reviews/2))
	random_list_neg = random.sample(range(int(len(full_review_list)/2),len(full_review_list)),int(no_reviews/2))

	review_list={}
	for i in random_list_pos:
		review_list[i]=list_review(full_review_list[i],indexlist)

	for i in random_list_neg:
		review_list[i]=list_review(full_review_list[i],indexlist)

	testfile = open('aclImdb_v1/aclImdb/test/labeledBow.feat','r',encoding='utf-8')
	test_review_list=testfile.readlines()

	validation_list_pos=random.sample(range(0,int(len(full_review_list)/2)),int(no_validation/2))
	validation_list_neg= random.sample(range(int(len(full_review_list)/2),len(full_review_list)),int(no_validation/2))
	validation_list = validation_list_pos+validation_list_neg

	validation_reviews={}
	for i in validation_list:
		validation_reviews[i]=list_review(full_review_list[i],indexlist)

	test_list_pos=random.sample(range(0,int(len(test_review_list)/2)),int(no_test/2))
	test_list_neg= random.sample(range(int(len(test_review_list)/2),len(test_review_list)),int(no_test/2))
	test_list=test_list_neg+test_list_pos

	test_reviews={}

	for i in test_list:
		test_reviews[i]=list_review(test_review_list[i],indexlist)

	save(validation_reviews,'validationreviews.pkl')
	save(validation_list,'validationlist.pkl')
	save(test_reviews,'testreviews.pkl')
	save(test_list,'testlist.pkl')
	save(random_list_pos,'randompos.pkl')
	save(random_list_neg,'randomneg.pkl')
	save(review_list,'reviewlist.pkl')
	save(indexlist,'indexlist.pkl')



if __name__=="__main__":
	preprocess()
	

















